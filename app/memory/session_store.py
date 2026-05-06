from collections import defaultdict
from datetime import datetime, timezone
from typing import Any


class SessionStore:
    def __init__(self) -> None:
        self._events: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def append(self, session_id: str, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        event = {
            "type": event_type,
            "payload": payload,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._events[session_id].append(event)
        return event

    def get(self, session_id: str) -> list[dict[str, Any]]:
        return list(self._events.get(session_id, []))

    def clear(self, session_id: str | None = None) -> None:
        if session_id:
            self._events.pop(session_id, None)
        else:
            self._events.clear()


session_store = SessionStore()
