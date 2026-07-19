# connection_service.py

from shared.services.base_service import (
    BaseService
)
from modules.connections import (
    Connection,
    ConnectionRepository
)
from modules.connections.connection_dto import ConnectionDTO

class ConnectionService(BaseService):

    def __init__(self, repository):
        super().__init__()
        self.repository = repository

    def get_connection(self):
        return self.repository.get_all()

    def info_connection(self, name: str):
        self.validate_required(name, "Nome da Conexão")
        self.info(f"Criando conexão: {name}")

    def create_connection(self, dto: ConnectionDTO):
        # BUG FIX: Implementação - Associando id_projeto ao criar conexão
        connection = Connection(
            id_projeto=dto.id_projeto,
            nm_conexao=dto.nm_conexao,
            tp_database=dto.tp_database,
            nm_host=dto.nm_host,
            nu_porta=dto.nu_porta,
            nm_database=dto.nm_database,
            nm_schema=dto.nm_schema,
            nm_usuario=dto.nm_usuario,
            tx_password=dto.tx_password,
            ds_caminho=dto.ds_caminho,
            ds_jdbc_driver=dto.ds_jdbc_driver,
            ds_jdbc_url=dto.ds_jdbc_url,
            fl_ativo=dto.fl_ativo
        )
        return self.repository.create(connection)

    def update_connection(self, dto: ConnectionDTO):
        connection = self.repository.get_by_id(dto.id_conexao)

        if not connection:
            raise Exception("Conexão não encontrada.")

        # BUG FIX: Implementação - Atualizando id_projeto da conexão
        connection.id_projeto = dto.id_projeto
        connection.nm_conexao = dto.nm_conexao
        connection.tp_database = dto.tp_database
        connection.nm_host = dto.nm_host
        connection.nu_porta = dto.nu_porta
        connection.nm_database = dto.nm_database
        connection.nm_schema = dto.nm_schema
        connection.nm_usuario = dto.nm_usuario
        connection.tx_password = dto.tx_password
        connection.ds_caminho = dto.ds_caminho
        connection.ds_jdbc_driver = dto.ds_jdbc_driver
        connection.ds_jdbc_url = dto.ds_jdbc_url
        connection.fl_ativo = dto.fl_ativo

        self.repository.update()

    def delete_connection(self, id_conexao: int):
        connection = (self.repository.get_by_id(id_conexao))

        if not connection:
            raise Exception("Conexão não encontrada.")

        self.repository.delete(connection)

    def get_connection_by_id(self, id_conexao):
        return self.repository.get_by_id(id_conexao)

    # BUG FIX: Implementação - Expor verificação de duplicidade de conexão
    def check_duplicate(self, nm_conexao, tp_database, nm_host, nu_porta, nm_database, nm_schema, nm_usuario, tx_password, ds_caminho) -> bool:
        return self.repository.check_duplicate(
            nm_conexao=nm_conexao,
            tp_database=tp_database,
            nm_host=nm_host,
            nu_porta=nu_porta,
            nm_database=nm_database,
            nm_schema=nm_schema,
            nm_usuario=nm_usuario,
            tx_password=tx_password,
            ds_caminho=ds_caminho
        )
