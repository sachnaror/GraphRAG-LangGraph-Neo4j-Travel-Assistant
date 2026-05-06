from fastapi import FastAPI

from app.api.routes_health import router as health_router
from app.api.routes_travel import router as travel_router


app = FastAPI(
    title="GraphRAG LangGraph Neo4j Travel Assistant",
    description="GraphRAG-style travel decision engine with mock graph/RAG fallbacks.",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(travel_router)
