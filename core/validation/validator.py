# validator.py

from __future__ import annotations
from abc import ABC, abstractmethod
from .validation_report import ValidationReport

class Validator(ABC):
    # Classe base para validações.
    def __init__(self) -> None:
        self._report = ValidationReport()

    @abstractmethod
    def validate(self, dto) -> ValidationReport:
        # Executa a validação.
        raise NotImplementedError()

    def reset(self):
        self._report.clear()

    @property
    def report(self) -> ValidationReport:
        return self._report

    @property
    def valid(self):
        return self._report.valid

    @property
    def invalid(self) -> bool:
        return not self._report.valid
