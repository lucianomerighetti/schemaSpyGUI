# validation_report.py

from __future__ import annotations
from dataclasses import (
    dataclass,
    field
)
from .validation_result import ValidationResult
from .validation_severity import ValidationSeverity

@dataclass(slots=True)
class ValidationReport:
    results: list[ValidationResult] = field(default_factory=list)

    # Inclusão
    def add(self, result: ValidationResult) -> None:
        self.results.append(result)

    def error(self, field: str, message: str, *, code: str = "") -> None:
        self.results.append(ValidationResult.error(field=field, message=message, code=code))

    def warning(self, ield: str, message: str, *, code: str = "") -> None:
        self.results.append(ValidationResult.warning(field=field, message=message, code=code))

    def info(self, message: str) -> None:
        self.results.append(ValidationResult.info(message))

    def success(self, message: str = "") -> None:
        self.results.append(ValidationResult.success(message))

    # Propriedades
    @property
    def valid(self) -> bool:
        return not any(r.has_error for r in self.results)

    @property
    def has_errors(self) -> bool:
        return any(r.has_error for r in self.results)

    @property
    def has_warnings(self) -> bool:
        return any(r.has_warning for r in self.results)

    @property
    def has_infos(self) -> bool:
        return any(r.has_info for r in self.results)

    @property
    def errors(self) -> list[ValidationResult]:
        return [r for r in self.results if r.has_error]

    @property
    def warnings(self) -> list[ValidationResult]:
        return [r for r in self.results if r.has_warning]

    @property
    def infos(self) -> list[ValidationResult]:
        return [r for r in self.results if r.has_info]

    @property
    def first_error(self) -> ValidationResult | None:
        for result in self.results:
            if result.has_error:
                return result
        return None

    @property
    def first_warning(self) -> ValidationResult | None:
        for result in self.results:
            if result.has_warning:
               return result
        return None

    def clear(self) -> None:
        self.results.clear()

    def __len__(self) -> int:
        return len(self.results)

    def __iter__(self):
        return iter(self.results)

    def __bool__(self) -> bool:
        return self.valid