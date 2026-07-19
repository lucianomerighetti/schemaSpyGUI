# settings_viewmodel.py
from shared.viewmodels.base_viewmodel import BaseViewModel
from .setting_dto import SettingDTO

class SettingViewModel(BaseViewModel):
    def __init__(self, service):
        super().__init__()
        self.service = service

    def get_setting_by_id(self, id_setting):
        return self.service.get_setting_by_id(id_setting)

    def create_setting(self, dto: SettingDTO):
        return self.service.create_setting(dto)

    def read_setting(self):
        return self.service.get_settings()

    def update_setting(self, dto: SettingDTO):
        return self.service.update_setting(dto)

    def delete_setting(self, id_setting: int):
        return self.service.delete_setting(id_setting)

    def get_setting_by_name(self, nm_setting: str):
        return self.service.get_setting_by_name(nm_setting)