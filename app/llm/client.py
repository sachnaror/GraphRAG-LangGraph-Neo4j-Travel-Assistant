from openai import OpenAI

from app.config import get_settings
from app.llm.output_parser import parse_explanation
from app.llm.prompts import build_flight_explanation_prompt
from app.mocks.mock_llm import explain_choice


def generate_explanation(
    best_flight: dict,
    alternatives: list[dict],
    comparison: list[dict],
    priority: str,
    context: list[str] | None = None,
) -> str:
    settings = get_settings()

    if not settings.openai_api_key:
        return explain_choice(best_flight, priority)

    prompt = build_flight_explanation_prompt(
        best_flight=best_flight,
        alternatives=alternatives,
        comparison=comparison,
        priority=priority,
        context=context,
    )

    try:
        client = OpenAI(api_key=settings.openai_api_key, timeout=12)
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "You explain travel recommendations clearly and honestly.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        content = response.choices[0].message.content
        if content:
            return parse_explanation(content)
    except Exception:
        pass

    return explain_choice(best_flight, priority)
