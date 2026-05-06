# GraphRAG-LangGraph-Neo4j-Travel-Assistant

An intelligent travel decision engine that uses a GraphRAG-style flow to plan, rank, validate, compare, and explain flight options.

The current local implementation runs as an agentic GraphRAG prototype with JSON-backed graph/mock data, FAISS-backed local vector retrieval over travel documents, deterministic scoring, optional Neo4j graph ingestion, and an OpenAI explanation layer with mock fallback.

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

(1) main.py
   ↓
(2) API Routes
   ↓
(3) Pydantic Schemas
   ↓
(4) Services
   ↓
(5) Orchestrator
   ↓
(6) Workflow Engine
   ↓
(7) GraphRAG Flow
   ↓
(8) Validation Agent
   ↓
(9) Graph + RAG Retrieval
   ↓
(10) Planner Agent
   ↓
(11) Scoring Engine
   ↓
(12) Comparison Engine
   ↓
(13) LLM Layer
   ↓
(14) Session Memory
```

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

├── GraphRAG-LangGraph-Neo4j-Travel-Assistant/
│
│   ├── README.md                                # Complete architecture, setup guide, APIs, FAISS workflow, screenshots
│   ├── requirements.txt                         # Python dependencies
│   ├── .env                                     # Real local secrets (never commit)
│   ├── example.env                              # Sample environment variables template
│   ├── .gitignore                               # Ignore secrets, caches, FAISS artifacts, virtual env
│
│   ├── app/
│   │
│   │   ├── main.py (1)                          # FastAPI application entrypoint, middleware, startup hooks
│   │   ├── config.py (1.1)                      # Central configuration loader, FAISS/docs/index env paths
│   │
│   │   ├── utils/
│   │   │   ├── logger.py (1.2)                  # Structured logging setup
│   │   │   └── helpers.py (1.3)                 # Shared helper utilities and reusable functions
│   │
│   │   ├── observability/
│   │   │   └── metrics.py (1.4)                 # Prometheus/custom metrics and monitoring hooks
│   │
│   │   ├── api/
│   │   │   ├── routes_health.py (2.1)           # Health check endpoints for monitoring/K8s probes
│   │   │   └── routes_travel.py (2.2)           # Main travel assistant REST APIs
│   │
│   │   ├── schemas/
│   │   │   └── travel.py (3)                    # Pydantic request/response models
│   │
│   │   ├── services/
│   │   │   ├── travel_service.py (4)            # Core business logic layer
│   │   │   ├── validation_service.py (8.1)      # Rule validation and business validation engine
│   │   │   ├── scoring_service.py (11)          # Flight ranking and scoring calculations
│   │   │   └── comparison_service.py (12)       # Multi-flight comparison engine
│   │
│   │   ├── agents/
│   │   │   ├── orchestrator.py (5)              # Central controller coordinating all agents/workflows
│   │   │   ├── planner_agent.py (6)             # AI reasoning agent for itinerary planning
│   │   │   ├── validator_agent.py (7)           # AI validation/checking agent
│   │   │   ├── graph_agent.py (9.1)             # Neo4j graph traversal and relationship reasoning
│   │   │   └── rag_agent.py (9.2)               # Semantic RAG retrieval agent
│   │
│   │   ├── workflows/
│   │   │   ├── travel_workflow.py (6.1)         # LangGraph workflow state transitions
│   │   │   └── graph_rag_flow.py (6.2)          # Combined GraphRAG execution pipeline
│   │
│   │   ├── graph/
│   │   │   ├── models.py (9.1.1)                # Graph entities and relationship definitions
│   │   │   ├── neo4j_client.py (9.1.2)          # Neo4j database connection/session management
│   │   │   └── queries.py (9.1.3)               # Cypher queries for graph search/traversal
│   │
│   │   ├── retrieval/
│   │   │   ├── retriever.py (9.2.1)             # Loads/searches FAISS index with fallback document retrieval
│   │   │   ├── vector_store.py (9.2.2)          # FAISS index creation, persistence, loading, vector search
│   │   │   └── embeddings.py (9.2.3)            # Embedding generation logic
│   │
│   │   ├── caching/
│   │   │   └── cache.py (9.2.2.1)               # Redis/local caching layer
│   │
│   │   ├── data/
│   │   │
│   │   │   ├── documents/
│   │   │   │   ├── pricing_notes.txt (9.2.3.1.1)# Airline pricing rules and fare notes
│   │   │   │   ├── airline_policies.txt (9.2.3.1.2)# Refund, baggage, and airline policy rules
│   │   │   │   └── travel_rules.txt (9.2.3.1.3)# Travel restrictions and compliance rules
│   │   │
│   │   │   ├── embeddings/
│   │   │   │
│   │   │   │   └── faiss_index/
│   │   │   │       ├── index.faiss (9.2.4.1.1) # Persisted FAISS vector index for semantic retrieval
│   │   │   │       ├── chunks.json (9.2.4.1.2) # Text chunks mapped to embeddings
│   │   │   │       ├── manifest.json (9.2.4.1.3)# Metadata/version info for FAISS build
│   │   │   │       └── .gitkeep (9.2.4.1.4)    # Preserve empty FAISS directory in Git
│   │
│   │   ├── llm/
│   │   │   ├── client.py (13)                   # OpenAI/LLM provider integration
│   │   │   ├── prompts.py (13.1)                # Prompt templates and system prompts
│   │   │   └── output_parser.py (13.2)          # Structured output parsing and Pydantic conversion
│   │
│   │   ├── mocks/
│   │   │   ├── mock_llm.py (13.3)               # Mock LLM responses for offline/local testing
│   │   │   └── mock_external_api.py (13.4)      # Mock airline/travel external APIs
│   │
│   │   ├── memory/
│   │   │   └── session_store.py (14)            # User memory/session persistence
│
│   ├── scripts/
│   │   ├── ingest_graph.py (15.1)               # Load JSON datasets into Neo4j
│   │   ├── run_demo_queries.py (15.2)           # Run sample GraphRAG demo queries
│   │   └── build_faiss_index.py (15.3)          # Build/rebuild FAISS index from documents
│
│   ├── tests/
│   │   └── test_retrieval.py (16)               # Tests FAISS retrieval and fallback indexing
│
│   ├── external_data/
│   │
│   │   ├── graph_data/
│   │   │   ├── users.json (17.1.1)              # User travel preference graph seed data
│   │   │   ├── flights.json (17.1.2)            # Flight graph dataset
│   │   │   ├── routes.json (17.1.3)             # Airline route relationship mappings
│   │   │   └── airports.json (17.1.4)           # Airport metadata and graph nodes
│   │
│   │   ├── api_mock/
│   │   │   ├── users.json (17.2.1)              # Mock API user responses
│   │   │   ├── flights.json (17.2.2)            # Mock API flight responses
│   │   │   ├── routes.json (17.2.3)             # Mock API route responses
│   │   │   └── airports.json (17.2.4)           # Mock API airport responses
│
│   ├── .venv/                                   # Local Python virtual environment
│   └── .pytest_cache/                           # Pytest cache files

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
| Embeddings | `data/embeddings/faiss_index` | Persisted FAISS index files and chunk metadata |

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

Build or rebuild the local FAISS index:

```bash
python scripts/build_faiss_index.py
```

Optional custom paths:

```bash
python scripts/build_faiss_index.py --documents-dir data/documents --index-dir data/embeddings/faiss_index
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
RETRIEVAL_DOCUMENTS_DIR=
RETRIEVAL_INDEX_DIR=
RETRIEVAL_BUILD_ON_STARTUP=false
```

`.env` is ignored by git. Keep real secrets only in `.env` or your local shell environment.

At runtime, retrieval prefers the persisted FAISS index in `data/embeddings/faiss_index`. If the index files are missing, the app falls back to building the store from `data/documents`. If `RETRIEVAL_BUILD_ON_STARTUP=true`, that fallback build is also saved back to disk automatically.

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
