# user_rule.py

from core.validation.validation_rule import ValidationRule
from core.validation.validation_report import ValidationReport
from typing import Any

class UserRule(ValidationRule):
    def validate(self, dto: Any, report: ValidationReport) -> None:
        # BUG FIX Regra vazia anteriormente (apenas comentário). Código antes da correção: (arquivo vazio)
        is_file_db = hasattr(dto, 'is_file_database') and dto.is_file_database
        if not is_file_db:
            if not hasattr(dto, 'nm_usuario') or not dto.nm_usuario or not dto.nm_usuario.strip():
                report.error("nm_usuario", "Usuário é obrigatório para bancos cliente/servidor.")