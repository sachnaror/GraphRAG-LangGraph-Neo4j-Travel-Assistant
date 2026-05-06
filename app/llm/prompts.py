def build_flight_explanation_prompt(
    best_flight: dict,
    alternatives: list[dict],
    comparison: list[dict],
    priority: str,
    context: list[str] | None = None,
) -> str:
    return f"""
You are a travel planning assistant. Explain why the selected flight is the best option.

User priority: {priority}

Best flight:
{best_flight}

Alternatives:
{alternatives}

Comparison:
{comparison}

Retrieved travel context:
{context or []}

Write a concise explanation in 3-5 sentences. Mention the flight number, price, duration,
reliability, and the tradeoff against alternatives. Do not invent fields that are missing.
""".strip()
