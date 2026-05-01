from app.services.travel_service import plan_trip

queries = [
    {"from": "Delhi", "to": "Mumbai", "type": "cheapest"},
    {"from": "Delhi", "to": "Mumbai", "type": "fastest"},
    {"from": "Delhi", "to": "Mumbai", "type": "business"}
]

for q in queries:
    print("\n==============================")
    print(f"Query: {q}")
    result = plan_trip(q)
    print("Result:", result)
