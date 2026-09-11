import json
from typing import Any, Dict, Optional
import httpx
from services.api.config import get_settings
from services.api.privacy.redactor import PrivacyRedactor


class PrivacyGateError(Exception):
    """Raised when an outbound payload fails the privacy redaction gate."""
    pass


class ModelUnavailableError(Exception):
    """The configured remote model cannot be used safely."""


class OpenRouterClient:
    """Wrapped OpenRouter client with privacy gate enforcement and zero-retention headers."""

    def __init__(self):
        self.settings = get_settings()
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.settings.openrouter_api_key}",
            "HTTP-Referer": "https://eduquery.daanish.edu.pk",
            "X-Title": "EduQuery AI Engine",
            "Content-Type": "application/json",
        }

    @property
    def is_configured(self) -> bool:
        return bool(
            self.settings.external_model_enabled
            and self.settings.openrouter_api_key
            and not self.settings.openrouter_api_key.startswith("sk-or-v1-demo")
        )

    @staticmethod
    def _build_payload(
        prompt: str,
        system_prompt: Optional[str],
        response_schema: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": "openai/gpt-5.6-luna-pro",
            "messages": [
                {"role": "system", "content": system_prompt or "You are an academic database assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
            "provider": {"zdr": True},
        }
        if response_schema:
            payload["response_format"] = {"type": "json_schema", "json_schema": response_schema}
        return payload

    async def generate_completion(
        self, prompt: str, system_prompt: Optional[str] = None, response_schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if not self.settings.external_model_enabled:
            raise ModelUnavailableError(
                "External model calls are disabled. Set EXTERNAL_MODEL_ENABLED=true only for an approved live check."
            )

        # 1. Redact prompt
        redacted_prompt, _ = PrivacyRedactor.redact_prompt(prompt)

        # 2. Privacy gate safety check
        if PrivacyRedactor.contains_pii(redacted_prompt):
            raise PrivacyGateError(
                "Privacy Gate Assertion Failed: Outbound payload contains unredacted PII."
            )

        # Demo authentication and remote model use are deliberately separate.
        if not self.settings.openrouter_api_key or self.settings.openrouter_api_key.startswith("sk-or-v1-demo"):
            raise ModelUnavailableError("OPENROUTER_API_KEY is not configured.")

        # 4. Production API call
        payload = self._build_payload(redacted_prompt, system_prompt, response_schema)

        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(self.api_url, json=payload, headers=self.headers, timeout=15.0)
                res.raise_for_status()
                return res.json()
        except httpx.HTTPError as exc:
            raise ModelUnavailableError("OpenRouter request failed.") from exc

    async def plan_query(self, prompt: str, system_prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.generate_completion(prompt, system_prompt, schema)
        try:
            content = response["choices"][0]["message"]["content"]
            return json.loads(content)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise ModelUnavailableError("OpenRouter returned an invalid structured plan.") from exc
