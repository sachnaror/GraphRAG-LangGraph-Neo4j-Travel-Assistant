def build_comparison(options: list[dict]) -> list[dict]:
    if not options:
        return []

    cheapest = min(options, key=lambda option: option["price"])["flight_no"]
    fastest = min(options, key=lambda option: option["duration_minutes"])["flight_no"]
    best_rated = max(options, key=lambda option: option.get("rating") or 0)["flight_no"]
    best_overall = max(options, key=lambda option: option.get("score", 0))["flight_no"]

    comparison = []
    for option in options:
        labels = []
        if option["flight_no"] == best_overall:
            labels.append("Best Overall")
        if option["flight_no"] == cheapest:
            labels.append("Cheapest")
        if option["flight_no"] == fastest:
            labels.append("Fastest")
        if option["flight_no"] == best_rated:
            labels.append("Best Rated")

        comparison.append(
            {
                "flight_no": option["flight_no"],
                "price": option["price"],
                "duration_minutes": option["duration_minutes"],
                "rating": option.get("rating"),
                "score": option.get("score", 0),
                "highlight": ", ".join(labels) or "Alternative",
            }
        )

    return comparison
