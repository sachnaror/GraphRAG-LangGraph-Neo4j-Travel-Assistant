from app.mocks.mock_external_api import get_user


def build_options(route_options: list[dict], request: dict, context: list[str] | None = None) -> list[dict]:
    user = get_user(request.get("user_id"))
    priority = request.get("priority") or request.get("type") or (user or {}).get("priority") or "balanced"

    planned = []
    for option in route_options:
        enriched = dict(option)
        enriched["priority"] = priority
        enriched["rag_context"] = context or []
        enriched["user_profile"] = user or {}
        planned.append(enriched)
    return planned
