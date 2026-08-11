from dataclasses import dataclass, field
from typing import Any, Dict
import datetime

@dataclass(frozen=True)
class Signal:
    sursa: str
    topic: str
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    @property
    def sdi(self) -> float:
        return float(self.payload.get("sdi_estimat", 0.2))