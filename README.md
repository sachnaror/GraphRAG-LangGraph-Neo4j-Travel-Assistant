# GraphRAG-LangGraph-Neo4j-Travel-Assistant

## 🚀 Overview
An intelligent travel assistant combining GraphRAG, Neo4j, LangGraph agents, and LLMs to generate optimized travel plans.

## 🧠 How It Works
User query → Agents → Neo4j (graph data) + Mock APIs (RAG) → Reasoning → Ranking → LLM → Response

## 📁 Project Structure

I will add this shortly after completion and running it successfuly on local

# GraphRAG-LangGraph-Neo4j-Travel-Assistant

## 🚀 Overview
An intelligent travel decision engine built using:
- GraphRAG (Graph + Retrieval Augmented Generation)
- Neo4j (relationship graph)
- LangGraph agents (orchestration)
- LLM (reasoning + explanation)

It does not just search flights — it **reasons, ranks, validates, and explains decisions**.

---

## 🧠 What It Does
- Multi-hop reasoning (direct + layover routes)
- Constraint validation (baggage, seats, refund)
- Dynamic scoring (price, time, rating)
- Graph-based personalization (user preferences)
- LLM-based explanation (“Why this flight is best”)
- Fallback system (mock data if API/DB fails)

---

## 📁 Directory Structure & Execution Flow

```
main.py (1)
→ routes_travel.py (2)
→ travel_service.py (3)
→ graph_agent (4)
→ rag_agent (5)
→ planner_agent (6)
→ validator_agent (7)
→ scoring_service (8)
→ comparison_service (9)
→ llm (10)
→ schema response (11)
```

---

## 🏗️ Architecture Diagram

User → API → Service → Agents → Data (Neo4j + RAG)
→ Validation → Scoring → LLM → Response

---

## 🔄 Runtime Flow

1. User sends request
2. FastAPI receives request
3. travel_service orchestrates flow
4. graph_agent fetches Neo4j data (fallback to mock if needed)
5. rag_agent fetches external/docs
6. planner_agent builds options
7. validator filters invalid
8. scoring ranks options
9. comparison builds alternatives
10. LLM explains result
11. Response returned

---

## 🔁 Fallback Logic

If Neo4j fails:
→ use mock_external_api (data/api_mock)

If API fails:
→ use local JSON

---

## 📊 Data Sources

| Source | Usage |
|------|------|
| graph_data | Neo4j ingestion |
| api_mock | runtime fallback |
| documents | RAG knowledge |

---

## 🧪 Sample API Response

```json
{
  "best_flight": {
    "flight_no": "FL101",
    "from_city": "Delhi",
    "to_city": "Mumbai",
    "price": 5500,
    "duration_minutes": 130,
    "rating": 4.2,
    "on_time_performance": 0.92
  },
  "alternatives": [
    {
      "flight_no": "FL105",
      "from_city": "Delhi",
      "to_city": "Mumbai",
      "price": 4800,
      "duration_minutes": 180,
      "rating": 3.9
    }
  ],
  "comparison": [
    {
      "flight_no": "FL101",
      "price": 5500,
      "duration_minutes": 130,
      "rating": 4.2,
      "score": 0.82,
      "highlight": "Best Overall"
    }
  ],
  "explanation": "This flight is best due to balance of speed, cost, and reliability."
}
```

---

## 🤖 “Why this flight is best” (LLM Output Example)

```
We selected flight FL101 because it offers the best balance between travel time, cost, and reliability.

- Short duration (130 mins)
- High on-time performance (92%)
- Competitive pricing

This makes it ideal for business travel.
```

---

## 📡 cURL Request Example

```bash
curl -X POST "http://127.0.0.1:8000/plan-trip" \
-H "Content-Type: application/json" \
-d '{
  "from": "Delhi",
  "to": "Mumbai",
  "user_id": "U1",
  "priority": "time"
}'
```

---

## 🖥️ Sample Terminal Output

```
Query: Delhi → Mumbai

Best Flight: FL101
Price: 5500
Duration: 130 mins

Explanation:
Best balance of speed and reliability.
```

---

## ⚙️ How to Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🧪 Demo Script

```bash
python scripts/run_demo_queries.py
```

---

## 🎯 Final Summary

This system:
- Thinks (agents)
- Retrieves (RAG)
- Reasons (graph)
- Decides (scoring)
- Explains (LLM)

Unlike traditional systems, it answers **WHY**, not just **WHAT**.

---



## 🧑‍💻 Author


| Name              | Details                             |
|-------------------|-------------------------------------|
| **👨‍💻 Developer**  | Sachin Arora                      |
| **📧 Email**      | [sachnaror@gmail.com](mailto:sacinaror@gmail.com) |
| **📍 Location**   | Noida, India                       |
| **📂 GitHub**     | [Link](https://github.com/sachnaror) |
| **🌐 Youtube**    | [Link](https://www.youtube.com/@sachnaror4841/videos) |
| **🌐 Blog**       | [Link](https://medium.com/@schnaror) |
| **🌐 Website**    | [Link](https://about.me/sachin-arora) |
| **🌐 Twitter**    | [Link](https://twitter.com/sachinhep) |
| **📱 Phone**      | [+91 9560330483](tel:+919560330483) |


------------------------------------------------------------------------
