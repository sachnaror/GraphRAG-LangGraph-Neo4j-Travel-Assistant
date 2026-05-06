def parse_explanation(raw_text: str | None) -> str:
    if not raw_text:
        return ""

    text = raw_text.strip()
    prefixes = ["Explanation:", "Response:", "Answer:"]
    for prefix in prefixes:
        if text.lower().startswith(prefix.lower()):
            text = text[len(prefix) :].strip()

    return text
