# setting_validator.py
from __future__ import annotations
from core.validation.validator import Validator
from core.validation.validation_report import ValidationReport
from .setting_dto import SettingDTO

class SettingValidator(Validator):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, dto: SettingDTO) -> ValidationReport:
        self.reset()
        if not dto.nm_setting or not dto.nm_setting.strip():
            self.report.error("nm_setting", "Nome da configuração é obrigatório.")
        return self.report
