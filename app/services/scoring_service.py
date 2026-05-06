def score_options(options: list[dict], priority: str = "balanced") -> list[dict]:
    if not options:
        return []

    priority = (priority or "balanced").lower()
    prices = [float(option["price"]) for option in options]
    durations = [float(option["duration_minutes"]) for option in options]
    ratings = [float(option.get("rating") or 0) for option in options]

    min_price, max_price = min(prices), max(prices)
    min_duration, max_duration = min(durations), max(durations)
    min_rating, max_rating = min(ratings), max(ratings)

    weights = _weights_for(priority)
    scored = []
    for option in options:
        price_score = 1 - _normalize(float(option["price"]), min_price, max_price)
        time_score = 1 - _normalize(float(option["duration_minutes"]), min_duration, max_duration)
        rating_score = _normalize(float(option.get("rating") or 0), min_rating, max_rating)
        reliability_score = float(option.get("on_time_performance") or 0)

        score = (
            price_score * weights["price"]
            + time_score * weights["time"]
            + rating_score * weights["rating"]
            + reliability_score * weights["reliability"]
        )
        enriched = dict(option)
        enriched["score"] = round(score, 3)
        scored.append(enriched)

    return sorted(scored, key=lambda option: option["score"], reverse=True)


def _normalize(value: float, minimum: float, maximum: float) -> float:
    if maximum == minimum:
        return 1.0
    return (value - minimum) / (maximum - minimum)


def _weights_for(priority: str) -> dict[str, float]:
    if priority in {"price", "cheapest"}:
        return {"price": 0.55, "time": 0.15, "rating": 0.15, "reliability": 0.15}
    if priority in {"time", "fastest"}:
        return {"price": 0.15, "time": 0.45, "rating": 0.15, "reliability": 0.25}
    if priority in {"business", "comfort"}:
        return {"price": 0.10, "time": 0.25, "rating": 0.30, "reliability": 0.35}
    return {"price": 0.30, "time": 0.30, "rating": 0.20, "reliability": 0.20}
