import re


def clean_text(raw: str) -> str:
    """Accept raw text input and perform minimal cleanup."""
    # Strip HTML tags if present
    text = re.sub(r"<[^>]+>", "", raw)
    # Normalize whitespace: collapse multiple spaces/newlines
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
