from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid


@dataclass(slots=True)
class Event:

    name: str

    payload: Any = None

    source: Any = None

    timestamp: datetime = field(default_factory=datetime.now)

    event_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )