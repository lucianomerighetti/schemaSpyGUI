# validation_severity.py

from enum import Enum

# Define o nível da validação.
class ValidationSeverity(str, Enum):
    # Severidade da validação.
    ERROR   = "error"
    WARNING = "warning"
    INFO    = "info"
    SUCCESS = "success"