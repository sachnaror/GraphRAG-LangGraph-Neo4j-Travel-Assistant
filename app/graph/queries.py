DIRECT_AND_ONE_HOP_ROUTES = """
CALL {
  MATCH (origin:Airport {city: $from_city})-[:HAS_FLIGHT]->(flight:Flight)-[:ARRIVES_AT]->(destination:Airport {city: $to_city})
  RETURN {
    flight_no: flight.flight_no,
    from_city: origin.city,
    to_city: destination.city,
    price: toFloat(flight.price),
    duration_minutes: toInteger(flight.duration_minutes),
    rating: toFloat(flight.rating),
    on_time_performance: toFloat(flight.on_time_performance),
    airline: flight.airline,
    is_direct: true,
    layovers: [],
    segments: [{
      flight_no: flight.flight_no,
      airline: flight.airline,
      from: origin.city,
      to: destination.city,
      seat_class: flight.seat_class,
      available_seats: {Economy: flight.available_economy, Business: flight.available_business},
      fare_rules: {refundable: flight.refundable, change_fee: flight.change_fee}
    }]
  } AS option

  UNION

  MATCH (origin:Airport {city: $from_city})-[:HAS_FLIGHT]->(first:Flight)-[:ARRIVES_AT]->(layover:Airport)
  MATCH (layover)-[:HAS_FLIGHT]->(second:Flight)-[:ARRIVES_AT]->(destination:Airport {city: $to_city})
  WHERE layover.city <> origin.city AND layover.city <> destination.city
  RETURN {
    flight_no: first.flight_no + '+' + second.flight_no,
    from_city: origin.city,
    to_city: destination.city,
    price: toFloat(first.price) + toFloat(second.price),
    duration_minutes: toInteger(first.duration_minutes) + toInteger(second.duration_minutes),
    rating: (toFloat(first.rating) + toFloat(second.rating)) / 2,
    on_time_performance: toFloat(first.on_time_performance) * toFloat(second.on_time_performance),
    airline: first.airline + ' + ' + second.airline,
    is_direct: false,
    layovers: [layover.city],
    segments: [
      {
        flight_no: first.flight_no,
        airline: first.airline,
        from: origin.city,
        to: layover.city,
        seat_class: first.seat_class,
        available_seats: {Economy: first.available_economy, Business: first.available_business},
        fare_rules: {refundable: first.refundable, change_fee: first.change_fee}
      },
      {
        flight_no: second.flight_no,
        airline: second.airline,
        from: layover.city,
        to: destination.city,
        seat_class: second.seat_class,
        available_seats: {Economy: second.available_economy, Business: second.available_business},
        fare_rules: {refundable: second.refundable, change_fee: second.change_fee}
      }
    ]
  } AS option
}
RETURN option
LIMIT $limit
"""


def route_parameters(request: dict, limit: int = 20) -> dict:
    return {
        "from_city": request.get("from") or request.get("from_city"),
        "to_city": request.get("to") or request.get("to_city"),
        "limit": limit,
    }
