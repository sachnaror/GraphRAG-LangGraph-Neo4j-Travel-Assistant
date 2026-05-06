from app.retrieval.retriever import get_document_retriever


def retrieve_context(request: dict) -> list[str]:
    priority = (request.get("priority") or request.get("type") or "").lower()
    query = _build_query(request)
    snippets = [
        f"[{result.source} score={result.score}] {result.text}"
        for result in get_document_retriever().retrieve(query, top_k=3)
    ]

    if priority == "business":
        snippets.append("Business travelers should favor reliability, time, and refundable fares.")
    elif priority in {"price", "cheapest"}:
        snippets.append("Budget-sensitive travelers should favor lower total fare.")
    elif priority in {"time", "fastest"}:
        snippets.append("Time-sensitive travelers should favor shorter duration and on-time performance.")

    return snippets


def _build_query(request: dict) -> str:
    from_city = request.get("from") or request.get("from_city") or ""
    to_city = request.get("to") or request.get("to_city") or ""
    priority = request.get("priority") or request.get("type") or "balanced"
    seat_class = request.get("seat_class") or ""
    refundable = "refundable" if request.get("refundable_only") else ""

    return " ".join(
        part
        for part in [from_city, to_city, priority, seat_class, refundable, "flight policy baggage pricing"]
        if part
    )
