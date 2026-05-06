from dataclasses import dataclass
from typing import Any

from app.config import get_settings
from app.graph.queries import DIRECT_AND_ONE_HOP_ROUTES, route_parameters


@dataclass
class Neo4jClient:
    uri: str | None
    username: str | None
    password: str | None

    @classmethod
    def from_settings(cls) -> "Neo4jClient":
        settings = get_settings()
        return cls(
            uri=settings.neo4j_uri,
            username=settings.neo4j_username,
            password=settings.neo4j_password,
        )

    @property
    def is_configured(self) -> bool:
        return bool(self.uri and self.username and self.password)

    def run_read_query(self, query: str, parameters: dict[str, Any]) -> list[dict]:
        if not self.is_configured:
            return []

        try:
            from neo4j import GraphDatabase
        except ModuleNotFoundError:
            return []

        with GraphDatabase.driver(self.uri, auth=(self.username, self.password)) as driver:
            with driver.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]

    def get_route_records(self, request: dict) -> list[dict]:
        return self.run_read_query(DIRECT_AND_ONE_HOP_ROUTES, route_parameters(request))
