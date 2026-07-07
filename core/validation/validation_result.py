# validation_result.py

from __future__ import annotations
from dataclasses import (
    dataclass,
    field as dc_field
)
from typing import Any
from unittest import result
from .validation_severity import ValidationSeverity

@dataclass(slots=True)
class ValidationResult:
    # Resultado de uma validação.
    valid:    bool = True
    field:    str = ""
    message:  str = ""
    severity: ValidationSeverity = ValidationSeverity.SUCCESS
    value:    Any = None
    code:     str = ""
    # BUG FIX O atributo field da classe sombreava a funcao field do modulo dataclasses no escopo da classe, gerando TypeError. Codigo antes da correcao: details:  list[str] = field(default_factory=list)
    details:  list[str] = dc_field(default_factory=list)

    # Métodos auxiliares
    @property
    def has_error(self) -> bool:
        return not self.valid

    @property
    def has_warning(self) -> bool:
        return self.severity == ValidationSeverity.WARNING

    @property
    def has_info(self) -> bool:
        return self.severity == ValidationSeverity.INFO

    @property
    def has_success(self) -> bool:
        return self.valid

    # Fábricas
    @classmethod
    def success(cls, message: str = "") -> "ValidationResult":
        return cls(valid=True, severity=ValidationSeverity.SUCCESS, message=message)

    @classmethod
    def error(cls, field: str, message: str, *, code: str = "") -> "ValidationResult":
        return cls(valid=False, field=field, message=message, severity=ValidationSeverity.ERROR, code=code)

    @classmethod
    def warning(cls, field: str, message: str, *, code: str = "") -> "ValidationResult":
        return cls(valid=True, field=field, message=message, severity=ValidationSeverity.WARNING, code=code)

    @classmethod
    def info(cls, message: str) -> "ValidationResult":
        return cls(valid=True, severity=ValidationSeverity.INFO, message=message)

    # Utilidades
    def add_detail(self, message: str) -> None:
        # Adiciona um detalhe complementar.
        self.details.append(message)

    def clear(self) -> None:
        # Reinicia o objeto.
        self.valid    = True
        self.field    = ""
        self.message  = ""
        self.severity = ValidationSeverity.SUCCESS
        self.value    = None
        self.code     = ""
        self.details.clear()

    def __bool__(self) -> bool:
        # Permite usa "if result:""
        return self.valid