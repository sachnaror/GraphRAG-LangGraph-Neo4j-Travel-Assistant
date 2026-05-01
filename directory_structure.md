├── GraphRAG-LangGraph-Neo4j-Travel-Assistant/
│   ├── requirements.txt
│   ├── README.md
│   ├── .env
│   ├── app/
│   │   └── main.py
│   │   ├── mocks/
│   │   │   └── mock_llm.py
│   │   ├── llm/
│   │   │   └── client.py
│   │   ├── memory/
│   │   │   └── session_store.py
│   │   ├── graph/
│   │   │   └── neo4j_client.py
│   │   ├── workflows/
│   │   │   └── travel_workflow.py
│   │   ├── agents/
│   │   │   └── graph_agent.py
│   │   ├── utils/
│   │   │   └── logger.py
│   │   ├── observability/
│   │   │   └── metrics.py
│   │   ├── schemas/
│   │   │   └── travel.py
│   │   ├── retrieval/
│   │   │   └── embeddings.py
│   │   ├── api/
│   │   │   └── routes_travel.py
│   │   ├── caching/
│   │   │   └── cache.py
│   │   ├── services/
│   │   │   ├── travel_service.py
│   │   │   └── scoring_service.py
│   ├── tests/
│   │   └── test_agents.py
│   ├── scripts/
│   │   └── ingest_graph.py
│   ├── data/
│   │   ├── embeddings/
│   │   │   ├── faiss_index/
│   │   │   │   └── .gitkeep
│   │   ├── graph_data/
│   │   │   └── airports.json
│   │   ├── api_mock/
│   │   │   ├── users.json
│   │   │   ├── flights.json
│   │   │   ├── routes.json
│   │   │   └── airports.json
│   │   ├── documents/
│   │   │   └── travel_rules.txt
