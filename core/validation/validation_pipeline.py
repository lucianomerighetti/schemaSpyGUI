# validation_pipeline.py
from __future__ import annotations
from collections.abc import Iterator
from typing import Any
from .validation_report import ValidationReport
from .validation_rule import ValidationRule

class ValidationPipeline:
    def __init__(self) -> None:
        self._rules: list[ValidationRule] = []

    # Propriedades
    @property
    def rules(self) -> list[ValidationRule]:
        return self._rules

    @property
    def count(self) -> int:
        return len(self._rules)

    @property
    def is_empty(self) -> bool:
        return len(self._rules) == 0

    # Manipulação
    def add(self, rule: ValidationRule) -> "ValidationPipeline":
        if not isinstance(rule, ValidationRule):
            raise TypeError(f"{type(rule).__name__} não herda de ValidationRule.")

        self._rules.append(rule)
        return self

    def extend(self, rules: list[ValidationRule]) -> "ValidationPipeline":
        for rule in rules:
            self.add(rule)

        return self

    def remove(self, rule_type: type[ValidationRule]) -> bool:
        for rule in self._rules:
            if isinstance(rule, rule_type):
                self._rules.remove(rule)
                return True
        return False

    def clear(self) -> None:
        self._rules.clear()

    # Execução
    def execute(self, dto: Any, report: ValidationReport) -> ValidationReport:
        for rule in self._rules:
            rule.validate(dto, report)

        return report

    # Utilidades
    def contains(self, rule_type: type[ValidationRule]) -> bool:
        return any(
            isinstance(rule, rule_type)
            for rule in self._rules
        )

    def index_of(self, rule_type: type[ValidationRule]) -> int:
        for index, rule in enumerate(self._rules):
            if isinstance(rule, rule_type):
                return index
        return -1

    # Métodos especiais
    def __len__(self) -> int:
        return len(self._rules)

    def __iter__(self) -> Iterator[ValidationRule]:
        return iter(self._rules)

    def __getitem__(self, index: int) -> ValidationRule:
        return self._rules[index]

    def __bool__(self) -> bool:
        return not self.is_empty

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__} (rules={len(self._rules)})")