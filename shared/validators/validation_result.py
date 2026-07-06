# validation_result.py

from typing import (
    Tuple
)

from dataclasses import (
    dataclass
)

@dataclass(slots=True)
class ValidationResult:
    valid: bool
    message: str = ""
        
def field_valid_error(value: str, field_name: str) -> None:
    if value is None:
        raise ValidationResult(False, f"Informe {field_name}.")
    if isinstance(value, str):
        if not str(value).strip():
            raise ValidationResult(False, f"Informe {field_name}.")

def field_valid(value: str, field_name: str) -> ValidationResult:
    if value is None:
        return ValidationResult(False, f"Informe {field_name}.")
    if isinstance(value, str):
        if not str(value).strip():
            return ValidationResult(False, f"Informe {field_name}.")
    return ValidationResult(True)