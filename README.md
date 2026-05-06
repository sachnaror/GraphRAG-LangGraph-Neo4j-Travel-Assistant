# GraphRAG-LangGraph-Neo4j-Travel-Assistant

An intelligent travel decision engine that uses a GraphRAG-style flow to plan, rank, validate, compare, and explain flight options.

The current local implementation runs as an agentic GraphRAG prototype with JSON-backed graph/mock data, local vector retrieval over travel documents, deterministic scoring, optional Neo4j graph ingestion, and an OpenAI explanation layer with mock fallback.

If `OPENAI_API_KEY` is available in the environment, the explanation layer uses OpenAI. If the key is missing or the API call fails, it falls back to the local mock explanation.

All API keys and secret values are loaded from `.env` via `load_dotenv()`.

---

## Overview

Traditional flight search usually returns matching flights. This assistant goes one step further:

- Finds direct and one-layover route options.
- Validates constraints such as seat class, available seats, and refundable fares.
- Scores flights by price, duration, rating, and reliability.
- Uses user priority such as `price`, `time`, `business`, or `comfort`.
- Compares alternatives with labels like `Best Overall`, `Cheapest`, and `Fastest`.
- Explains why the top option was selected.

---

## Architecture

```text
User Request
  -> FastAPI route
  -> Travel service
  -> Agent orchestrator
  -> Travel workflow
  -> GraphRAG flow
  -> Graph agent
  -> RAG agent
  -> Retriever + vector store + embeddings
  -> Planner agent
  -> Validator agent
  -> Scoring service
  -> Comparison service
  -> OpenAI LLM client or mock fallback
  -> Travel response schema
```

Runtime data flow:

```text
API request
  -> Neo4j route query or JSON graph/mock fallback
  -> local document retrieval
  -> route planning
  -> validation
  -> ranking
  -> explanation
  -> response
```

---

## Project Structure

```text
.
├── app
│   ├── agents
│   │   ├── graph_agent.py          # Builds direct and one-layover route options
│   │   ├── planner_agent.py        # Enriches route options with user/context data
│   │   ├── rag_agent.py            # Loads local policy/context snippets
│   │   └── validator_agent.py      # Filters invalid route options
│   ├── api
│   │   ├── routes_health.py        # GET /health
│   │   └── routes_travel.py        # POST /plan-trip
│   ├── graph
│   │   ├── models.py               # Typed graph domain models
│   │   ├── neo4j_client.py         # Optional Neo4j query client
│   │   └── queries.py              # Cypher route queries
│   ├── llm
│   │   ├── client.py               # OpenAI explanation client with mock fallback
│   │   └── prompts.py              # Prompt builder for flight explanations
│   ├── mocks
│   │   ├── mock_external_api.py    # JSON-backed fallback data loader
│   │   └── mock_llm.py             # Deterministic explanation generator
│   ├── retrieval
│   │   ├── embeddings.py           # Local hashing embeddings
│   │   ├── retriever.py            # Document retriever
│   │   └── vector_store.py         # In-memory vector store
│   ├── schemas
│   │   └── travel.py               # Pydantic response models
│   ├── services
│   │   ├── comparison_service.py   # Builds comparison table
│   │   ├── scoring_service.py      # Scores/ranks options
│   │   └── travel_service.py       # Main orchestration layer
│   └── main.py                     # FastAPI application
├── data
│   ├── api_mock                    # Runtime fallback JSON data
│   ├── documents                   # Local RAG policy/context documents
│   ├── embeddings                  # Reserved for vector indexes
│   └── graph_data                  # Data intended for graph ingestion
├── scripts
│   ├── ingest_graph.py             # Validate/dry-run/write graph data to Neo4j
│   └── run_demo_queries.py         # Local demo runner
├── tests
│   ├── test_agents.py
│   └── test_services.py
├── example.env                     # Environment variable template
├── requirements.txt
└── README.md
```

---

## Execution Flow

```text
app/main.py
  -> app/api/routes_travel.py
  -> app/services/travel_service.py
  -> app/agents/orchestrator.py
  -> app/workflows/travel_workflow.py
  -> app/workflows/graph_rag_flow.py
  -> agents: graph_agent, rag_agent, planner_agent, validator_agent
  -> retrieval: retriever, vector_store, embeddings
  -> app/services/scoring_service.py
  -> app/services/comparison_service.py
  -> app/llm/client.py or app/mocks/mock_llm.py
  -> app/schemas/travel.py
```

---

## Data Sources

| Source | Path | Usage |
| --- | --- | --- |
| Mock API data | `data/api_mock` | Runtime fallback data for flights, routes, users, and airports |
| Graph data | `data/graph_data` | Seed data intended for Neo4j ingestion |
| Documents | `data/documents` | Local RAG-style context and policy notes |
| Embeddings | `data/embeddings` | Reserved for vector index files |

---

## Graph Ingestion

Ingestion is optional for local development because the graph agent falls back to JSON data.

Dry-run validation checks all JSON files in `data/graph_data` without connecting to Neo4j:

```bash
python scripts/ingest_graph.py
```

Write graph data into Neo4j from the project root:

```bash
python scripts/ingest_graph.py --write
```

If you are already inside the `scripts` directory, run:

```bash
python ingest_graph.py --write
```

Before using `--write`, fill these values in `.env`:

```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
```

If Neo4j is not running on `localhost:7687`, `--write` will fail with a connection refused error. Start Neo4j first, for example with Docker:

```bash
docker run --name travel-neo4j \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:5
```

Then use:

```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
```

Neo4j Browser will be available at:

```text
http://localhost:7474
```

---

## How to Run

From the project root:

```bash
cd /Users/homesachin/Desktop/zoneone/practice/GraphRAG-LangGraph-Neo4j-Travel-Assistant
```

Create and activate a virtual environment if needed:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Optional OpenAI setup:

```bash
cp example.env .env
```

Then edit `.env`:

```bash
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
APP_SECRET_KEY=your_local_secret_key
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
```

`.env` is ignored by git. Keep real secrets only in `.env` or your local shell environment.

Optionally validate graph data before starting:

```bash
python scripts/ingest_graph.py
```

Optionally ingest graph data into Neo4j:

```bash
python scripts/ingest_graph.py --write
```

Start the API:

```bash
uvicorn app.main:app --reload
```

If your local Python environment has a `websockets.typing` mismatch, run the API without websocket support:

```bash
uvicorn app.main:app --reload --ws none
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Metrics snapshot:

```bash
curl http://127.0.0.1:8000/metrics
```

---

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `GET` | `/metrics` | In-memory counters and timings |
| `POST` | `/plan-trip` | Agentic GraphRAG travel planning |
| `GET` | `/docs` | Interactive FastAPI Swagger UI |
| `GET` | `/openapi.json` | OpenAPI schema |

Open the interactive docs:

```text
http://127.0.0.1:8000/docs
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Metrics:

```bash
curl http://127.0.0.1:8000/metrics
```

---

## API Examples

Basic time-priority trip:

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

Cheapest trip:

```bash
curl -X POST "http://127.0.0.1:8000/plan-trip" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "Delhi",
    "to": "Mumbai",
    "user_id": "U2",
    "priority": "price"
  }'
```

Business travel with session memory:

```bash
curl -X POST "http://127.0.0.1:8000/plan-trip" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "Delhi",
    "to": "Mumbai",
    "user_id": "U1",
    "priority": "business",
    "seat_class": "Business",
    "session_id": "demo-session"
  }'
```

Refundable-only trip:

```bash
curl -X POST "http://127.0.0.1:8000/plan-trip" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "Delhi",
    "to": "Mumbai",
    "priority": "time",
    "refundable_only": true
  }'
```

Supported request fields:

| Field | Example | Notes |
| --- | --- | --- |
| `from` | `Delhi` | Required origin city |
| `to` | `Mumbai` | Required destination city |
| `user_id` | `U1` | Optional user profile from `data/api_mock/users.json` |
| `session_id` | `demo-session` | Optional session memory key |
| `priority` | `time` | Optional: `price`, `cheapest`, `time`, `fastest`, `business`, `comfort`, `balanced` |
| `seat_class` | `Economy` | Optional seat-class constraint |
| `refundable_only` | `true` | Optional fare-rule constraint |

---

## Sample Response

```json
{
  "best_flight": {
    "flight_no": "FL101",
    "from_city": "Delhi",
    "to_city": "Mumbai",
    "price": 4000.0,
    "duration_minutes": 90,
    "rating": 3.8,
    "on_time_performance": 0.85
  },
  "alternatives": [
    {
      "flight_no": "FL102+FL105",
      "from_city": "Delhi",
      "to_city": "Mumbai",
      "price": 11500.0,
      "duration_minutes": 230,
      "rating": 4.05,
      "on_time_performance": 0.765
    }
  ],
  "comparison": [
    {
      "flight_no": "FL101",
      "price": 4000.0,
      "duration_minutes": 90,
      "rating": 3.8,
      "score": 0.812,
      "highlight": "Best Overall, Cheapest, Fastest"
    },
    {
      "flight_no": "FL102+FL105",
      "price": 11500.0,
      "duration_minutes": 230,
      "rating": 4.05,
      "score": 0.341,
      "highlight": "Best Rated"
    }
  ],
  "explanation": "We selected FL101 because it is the best fit for short travel time for this route...",
  "retrieved_context": [
    "[travel_rules.txt score=0.4472] Travel rule guide: ..."
  ]
}
```

---

## Demo Script

```bash
python scripts/run_demo_queries.py
```

Example terminal output:

```text
Query: {'from': 'Delhi', 'to': 'Mumbai', 'type': 'fastest'}
Best Flight: FL101
Price: 4000.0
Duration: 90 mins
Explanation: We selected FL101 because it is the best fit for short travel time for this route...
```

---

## Tests

```bash
pytest
```

Current test coverage verifies:

- Graph agent direct and layover route construction.
- Local vector retrieval over document data.
- Agent orchestrator GraphRAG state generation.
- Travel service response generation.
- Session memory.
- Graph ingestion dataset validation.
- Empty-route error handling.

---

## Current Status

Implemented:

- FastAPI app with `/health` and `/plan-trip`.
- Agent orchestrator, travel workflow, and GraphRAG flow.
- Typed graph models for airports, routes, flights, users, and route options.
- Local embeddings, vector store, and document retriever.
- Optional Neo4j ingest script and Cypher route query path.
- JSON-backed mock flight/user data loader.
- Direct and one-layover route planning.
- Validation, scoring, comparison, and explanation flow.
- OpenAI-backed explanation generation with mock fallback.
- Demo script and pytest coverage.

Next improvements:

- Add a Streamlit UI for demo usage.
- Add structured LLM evaluation tests for explanation quality.

---

## Author

| Name | Details |
| --- | --- |
| Developer | Sachin Arora |
| Email | [sachnaror@gmail.com](mailto:sachnaror@gmail.com) |
| Location | Noida, India |
| GitHub | [sachnaror](https://github.com/sachnaror) |
| YouTube | [sachnaror4841](https://www.youtube.com/@sachnaror4841/videos) |
| Blog | [Medium](https://medium.com/@schnaror) |
| Website | [about.me/sachin-arora](https://about.me/sachin-arora) |
| Twitter | [sachinhep](https://twitter.com/sachinhep) |
