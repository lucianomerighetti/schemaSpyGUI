# connection_service.py

from PyQt6.QtWidgets import (
    QMessageBox
)
from shared.services.base_service import (
    BaseService
)
from modules.connections import (
    Connection,
    ConnectionRepository
)

class ConnectionService(BaseService):

    def __init__(self, repository):
        super().__init__()
        self.repository = repository

    def get_connection(self):
        return self.repository.get_all()

    def info_connection(self, name: str):
        self.validate_required(name, "Nome da Conexão")
        self.info(f"Criando conexão: {name}")

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
        connection = Connection(
            nm_conexao=nm_conexao,
            tp_database=tp_database,
            nm_host=nm_host,
            nu_porta=nu_porta,
            nm_database=nm_database,
            nm_schema=nm_schema,
            nm_usuario=nm_usuario,
            tx_password=tx_password,
            ds_caminho=ds_caminho,
            ds_jdbc_driver=ds_jdbc_driver,
            ds_jdbc_url=ds_jdbc_url,
            fl_ativo=fl_ativo
        )
        return self.repository.create(connection)

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
        connection = (self.repository.get_by_id(id_conexao))

        if not connection:
            raise Exception("Conexão não encontrada.")

        connection.nm_conexao = nm_conexao
        connection.tp_database = tp_database
        connection.nm_host = nm_host
        connection.nu_porta = nu_porta
        connection.nm_database = nm_database
        connection.nm_schema = nm_schema
        connection.nm_usuario = nm_usuario
        connection.tx_password = tx_password
        connection.ds_caminho = ds_caminho
        connection.ds_jdbc_driver = ds_jdbc_driver
        connection.ds_jdbc_url = ds_jdbc_url
        connection.fl_ativo = fl_ativo

        self.repository.update()

    def delete_connection(self, id_conexao: int):
        connection = (self.repository.get_by_id(id_conexao))

        if not connection:
            raise Exception("Conexão não encontrada.")

        self.repository.delete(connection)

    def get_connection_by_id(self, id_conexao):
        return self.repository.get_by_id(id_conexao)
