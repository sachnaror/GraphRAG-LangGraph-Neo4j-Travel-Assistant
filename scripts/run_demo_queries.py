import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

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
    print("Best Flight:", result.best_flight.flight_no)
    print("Price:", result.best_flight.price)
    print("Duration:", result.best_flight.duration_minutes, "mins")
    print("Explanation:", result.explanation)
