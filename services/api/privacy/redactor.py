import re
from typing import Tuple

# Common Pakistani / Student PII regex patterns
ROLL_NO_PATTERN = re.compile(r"\b(?:roll\s*(?:no|number|\#)?\s*[:=]?\s*)(\d{4,10})\b", re.IGNORECASE)
CNIC_PATTERN = re.compile(r"\b\d{5}[-\s]?\d{7}[-\s]?\d\b")
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
PHONE_PATTERN = re.compile(r"\b(?:\+92|03)\d{2}[-\s]?\d{7}\b")

# Common student name regex heuristic (e.g. "student Ali Hassan", "marks for Sara Khan")
NAME_INTRO_PATTERN = re.compile(
    r"\b(?:student|for|of|marks\s+for|attendance\s+for)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)\b"
)


class PrivacyRedactor:
    """Local privacy redaction gate.

    Sanitizes natural language prompts BEFORE any external LLM service is called.
    Replaces student names, roll numbers, emails, phone numbers, and CNICs with
    semantic tokens.
    """

    @classmethod
    def redact_prompt(cls, prompt: str) -> Tuple[str, bool]:
        redacted = prompt
        was_redacted = False

        # Redact roll numbers
        if ROLL_NO_PATTERN.search(redacted):
            redacted = ROLL_NO_PATTERN.sub("rollno [ROLL_NO]", redacted)
            was_redacted = True

        # Redact emails
        if EMAIL_PATTERN.search(redacted):
            redacted = EMAIL_PATTERN.sub("[EMAIL]", redacted)
            was_redacted = True

        # Redact phone numbers
        if PHONE_PATTERN.search(redacted):
            redacted = PHONE_PATTERN.sub("[PHONE]", redacted)
            was_redacted = True

        # Redact CNICs
        if CNIC_PATTERN.search(redacted):
            redacted = CNIC_PATTERN.sub("[CNIC]", redacted)
            was_redacted = True

        # Redact student names
        def name_replacer(match):
            nonlocal was_redacted
            was_redacted = True
            prefix = match.group(0).split(match.group(1))[0]
            return f"{prefix}[STUDENT_NAME]"

        if NAME_INTRO_PATTERN.search(redacted):
            redacted = NAME_INTRO_PATTERN.sub(name_replacer, redacted)

        return redacted, was_redacted

    @classmethod
    def contains_pii(cls, text: str) -> bool:
        """Safety assertion check. Returns True if raw PII patterns remain."""
        if CNIC_PATTERN.search(text) or EMAIL_PATTERN.search(text) or PHONE_PATTERN.search(text):
            return True
        return False
