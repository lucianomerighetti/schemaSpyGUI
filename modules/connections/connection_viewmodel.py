# connection_viewmodel.py

from shared.viewmodels.base_viewmodel import (
    BaseViewModel
)

class ConnectionViewModel(BaseViewModel):

    def __init__(self, service):
        super().__init__()
        self.service = service

    def get_connection_by_id(self, id_conexao):
        return self.service.get_connection_by_id(id_conexao)

    def create_connection(
        self,
        nm_conexao,
        tp_database,
        nm_host,
        nu_porta,
        nm_database,
        nm_schema,
        nm_usuario,
        tx_password,
        ds_caminho="",
        ds_jdbc_driver="",
        ds_jdbc_url="",
        fl_ativo=True
    ):
        return self.service.create_connection(
            nm_conexao,
            tp_database,
            nm_host,
            nu_porta,
            nm_database,
            nm_schema,
            nm_usuario,
            tx_password,
            ds_caminho,
            ds_jdbc_driver,
            ds_jdbc_url,
            fl_ativo
        )

    def read_connection(self):
        return self.service.get_connection()

    def update_connection(
        self,
        id_conexao,
        nm_conexao,
        tp_database,
        nm_host,
        nu_porta,
        nm_database,
        nm_schema,
        nm_usuario,
        tx_password,
        ds_caminho="",
        ds_jdbc_driver="",
        ds_jdbc_url="",
        fl_ativo=True
    ):
        return self.service.update_connection(
            id_conexao,
            nm_conexao,
            tp_database,
            nm_host,
            nu_porta,
            nm_database,
            nm_schema,
            nm_usuario,
            tx_password,
            ds_caminho,
            ds_jdbc_driver,
            ds_jdbc_url,
            fl_ativo
        )

    def delete_connection(self, id_conexao):
        return self.service.delete_connection(id_conexao)