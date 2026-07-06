# connection_result.py
from dataclasses import dataclass

@dataclass
class ConnectionResult:
    success: bool
    message: str
    elapsed_ms: int = 0