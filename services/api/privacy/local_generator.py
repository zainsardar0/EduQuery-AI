"""Local generation helper.

Tries these options in order:
- Ollama CLI (if available on PATH) -> `ollama generate <model> --prompt '<prompt>'`
- Ollama HTTP API (if OLLAMA_URL configured)

The function exposed is generate_completion(prompt, system_prompt, settings) and returns the assistant text.

This is a best-effort local runtime wrapper; tweak to your local infrastructure and model names.
"""
from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import json
from typing import Optional

import requests


def _compose_prompt(system_prompt: Optional[str], user_prompt: str) -> str:
    if system_prompt:
        return f"System: {system_prompt}\n\n{user_prompt}"
    return user_prompt


def _try_ollama_cli(model: str, prompt: str) -> str:
    """Call ollama CLI if present. Returns text output or raises on error."""
    ollama_cmd = shutil.which("ollama")
    if not ollama_cmd:
        raise RuntimeError("ollama CLI not found on PATH")
    # Build a safe CLI invocation: use --json to make parsing easier if available
    # Note: Ollama CLI syntax can vary by version; this is a conservative approach.
    cmd = [ollama_cmd, "generate", model, "--prompt", prompt]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        out = result.stdout.strip()
        # If CLI printed JSON, try to parse
        try:
            data = json.loads(out)
            # best effort: extract a text field
            if isinstance(data, dict):
                for key in ("output", "text", "result", "content"):
                    if key in data:
                        return str(data[key])
            return out
        except Exception:
            return out
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"ollama CLI failed: {exc.stderr or exc.stdout}") from exc


def _try_ollama_http(ollama_url: str, model: str, prompt: str, temperature: float = 0.0, max_tokens: int = 512) -> str:
    """Call Ollama HTTP-style API. This is best-effort and may require adjusting path/payload for your Ollama version."""
    url = ollama_url.rstrip("/") + "/api/generate"
    payload = {"model": model, "prompt": prompt, "temperature": float(temperature), "max_tokens": int(max_tokens)}
    resp = requests.post(url, json=payload, timeout=60.0)
    resp.raise_for_status()
    j = resp.json()
    # best-effort extraction
    if isinstance(j, dict):
        for k in ("text", "output", "result", "content"):
            if k in j:
                return str(j[k])
        # sometimes response contains choices
        choices = j.get("choices") or j.get("outputs")
        if isinstance(choices, list) and choices:
            first = choices[0]
            if isinstance(first, dict):
                for k in ("text", "content", "output"):
                    if k in first:
                        return str(first[k])
            return str(first)
    return str(j)


def generate_completion(user_prompt: str, system_prompt: Optional[str], settings) -> str:
    """Generate completion using local runtime. Returns assistant text.

    settings: the Settings object from services.api.config.get_settings() — used for defaults.
    """
    prompt = _compose_prompt(system_prompt, user_prompt)
    model = os.environ.get("OLLAMA_MODEL") or getattr(settings, "ollama_model", "llama2")
    ollama_url = os.environ.get("OLLAMA_URL") or getattr(settings, "ollama_url", None)
    temperature = float(os.environ.get("GENERATOR_TEMPERATURE") or getattr(settings, "generator_temperature", 0.0))
    max_tokens = int(os.environ.get("GENERATOR_MAX_TOKENS") or getattr(settings, "generator_max_tokens", 512))

    # 1) try CLI
    try:
        return _try_ollama_cli(model, prompt)
    except Exception:
        pass

    # 2) try HTTP
    if ollama_url:
        try:
            return _try_ollama_http(ollama_url, model, prompt, temperature=temperature, max_tokens=max_tokens)
        except Exception as exc:
            raise RuntimeError(f"Ollama HTTP generation failed: {exc}") from exc

    raise RuntimeError("No local generation runtime available (ollama CLI not on PATH and OLLAMA_URL not configured)")
