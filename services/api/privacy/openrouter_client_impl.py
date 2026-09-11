from typing import Any, Dict, Optional
import httpx
from services.api.config import get_settings
from services.api.privacy.redactor import PrivacyRedactor


class PrivacyGateError(Exception):
    """Raised when an outbound payload fails the privacy redaction gate."""
    pass


class OpenRouterClient:
    """Wrapped OpenRouter client with privacy gate enforcement and zero-retention headers."""

    def __init__(self):
        self.settings = get_settings()
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        # Use configured OpenRouter API key from settings (set OPENROUTER_API_KEY / openrouter_api_key in config)
        auth_key = getattr(self.settings, "openrouter_api_key", None) or None
        auth_header = f"Bearer {auth_key}" if auth_key else ""
        self.headers = {
            "Authorization": auth_header,
            "HTTP-Referer": "https://eduquery.daanish.edu.pk",
            "X-Title": "EduQuery AI Engine",
            "X-Data-Collection": "deny",  # Zero-retention request header
            "Content-Type": "application/json",
        }

    async def generate_completion(
        self, prompt: str, system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        # 1. Redact prompt
        redacted_prompt, _ = PrivacyRedactor.redact_prompt(prompt)

        # 2. Privacy gate safety check
        if PrivacyRedactor.contains_pii(redacted_prompt):
            raise PrivacyGateError(
                "Privacy Gate Assertion Failed: Outbound payload contains unredacted PII."
            )

        # 3. Demo mode bypass (zero external network call)
        if self.settings.demo_mode:
            return {
                "id": "demo-comp-001",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": f"[DEMO_MODE] Generated intent response for redacted prompt: '{redacted_prompt}'",
                        }
                    }
                ],
                "usage": {"prompt_tokens": 15, "completion_tokens": 20, "total_tokens": 35},
            }

        # 4. Production API call
        payload = {
            "model": "openai/gpt-5.6-luna-pro",
            "messages": [
                {"role": "system", "content": system_prompt or "You are an academic database assistant."},
                {"role": "user", "content": redacted_prompt},
            ],
            # Deterministic settings to reduce hallucination
            "temperature": 0,
            "top_p": 1.0,
        }

        async with httpx.AsyncClient() as client:
            res = await client.post(self.api_url, json=payload, headers=self.headers, timeout=10.0)
            res.raise_for_status()
            return res.json()
