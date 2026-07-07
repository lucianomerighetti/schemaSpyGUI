# validator.py

from __future__ import annotations
from abc import ABC, abstractmethod
from .validation_report import ValidationReport
from .validation_pipeline import ValidationPipeline

class Validator(ABC):
    # Classe base para validações.
    def __init__(self) -> None:
        # BUG FIX Falta de inicialização do atributo pipeline. Código antes da correção: self._report = ValidationReport()
        self._report = ValidationReport()
        self.pipeline = ValidationPipeline()

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
