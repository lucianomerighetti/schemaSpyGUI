# base_service.py

from __future__ import (
    annotations
)

from typing import (
    Any
)

from loguru import (
     logger
)

from dataclasses import (
    dataclass,
    field
)
from typing import (
    Tuple,
    Optional
)

@dataclass
class ValidationResult:
    valid: bool = False
    message: str = ""

class BaseService:
    """
    Classe base para serviços da aplicação.
    """
    def __init__(self):

        self._logger = logger

    @property
    def logger(self):
        return self._logger

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def validate_required(self, value: Any, field_name: str) -> None:
        if value is None:
            raise ValueError(f"{field_name} é obrigatório.")
        if isinstance(value, str):
            if not value.strip():
                raise ValueError(f"{field_name} é obrigatório.")
