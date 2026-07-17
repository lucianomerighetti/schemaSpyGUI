# Artefato:  connection_viewmodel.py

from shared.viewmodels.base_viewmodel import (
    BaseViewModel
)
from .connection_dto import ConnectionDTO

class ConnectionViewModel(BaseViewModel):

    def __init__(self, service):
        super().__init__()
        self.service = service

    def get_connection_by_id(self, id_conexao):
        return self.service.get_connection_by_id(id_conexao)

    def create_connection(self, dto: ConnectionDTO):
        return self.service.create_connection(dto)

    def read_connection(self):
        return self.service.get_connection()

    def update_connection(self, dto: ConnectionDTO):
        return self.service.update_connection(dto)

    def delete_connection(self, id_conexao):
        return self.service.delete_connection(id_conexao)