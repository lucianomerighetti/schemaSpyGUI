# validation_rule.py

from __future__ import annotations
from abc import (
    ABC,
    abstractmethod
)
from typing import Any
from .validation_report import ValidationReport

class ValidationRule(ABC):
    @abstractmethod
    def validate(self, dto: Any, report: ValidationReport) -> None:
        raise NotImplementedError