def explain_choice(best_flight: dict, priority: str = "balanced") -> str:
    priority_text = {
        "price": "lowest practical fare",
        "cheapest": "lowest practical fare",
        "time": "short travel time",
        "fastest": "short travel time",
        "business": "reliability and comfort",
        "comfort": "comfort and rating",
    }.get((priority or "balanced").lower(), "overall balance")

    return (
        f"We selected {best_flight['flight_no']} because it is the best fit for {priority_text} "
        f"for this route. It costs INR {best_flight['price']:.0f}, takes "
        f"{best_flight['duration_minutes']} minutes, has a rating of "
        f"{best_flight.get('rating') or 'N/A'}, and shows "
        f"{round((best_flight.get('on_time_performance') or 0) * 100)}% on-time performance."
    )
