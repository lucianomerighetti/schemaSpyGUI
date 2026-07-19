# connection_repository.py

from sqlalchemy.orm import Session

from modules.connections import (
    Connection
)

class ConnectionRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return (
            self.session
            .query(Connection)
            .order_by(Connection.nm_conexao)
            .all()
        )

    def get_active(self):
        return (
            self.session
            .query(Connection)
            .filter(Connection.fl_ativo.is_(True))
            .order_by(Connection.nm_conexao)
            .all()
        )

    def get_by_id(self, id_conexao: int):
        return (
            self.session
            .query(Connection)
            .filter(Connection.id_conexao == id_conexao)
            .first()
        )

    def get_by_name(self, nm_conexao: str):
        return (
            self.session
            .query(Connection)
            .filter(Connection.nm_conexao == nm_conexao)
            .first()
        )

    def create(self, connection: Connection) -> Connection:
        self.session.add(connection)
        self.session.commit()
        self.session.refresh(connection)
        return connection

    def update(self):
        self.session.commit()

    def delete(self, connection: Connection):
        self.session.delete(connection)
        self.session.commit()

    def exists_by_name(self, nm_conexao: str) -> bool:
        return (
            self.session
            .query(Connection)
            .filter(Connection.nm_conexao == nm_conexao)
            .first()
            is not None
        )

    def count(self) -> int:
        return (
            self.session
            .query(Connection)
            .count()
        )

    def search(self, text: str):
        return (
            self.session
            .query(Connection)
            .filter(Connection.nm_conexao.ilike(f"%{text}%"))
            .order_by(Connection.nm_conexao)
            .all()
        )

    # BUG FIX: Implementação - Verificar se existe conexão duplicada baseada em todos os campos da UniqueConstraint
    def check_duplicate(self, nm_conexao, tp_database, nm_host, nu_porta, nm_database, nm_schema, nm_usuario, tx_password, ds_caminho) -> bool:
        return (
            self.session
            .query(Connection)
            .filter(
                Connection.nm_conexao == nm_conexao,
                Connection.tp_database == tp_database,
                Connection.nm_host == nm_host,
                Connection.nu_porta == nu_porta,
                Connection.nm_database == nm_database,
                Connection.nm_schema == nm_schema,
                Connection.nm_usuario == nm_usuario,
                Connection.tx_password == tx_password,
                Connection.ds_caminho == ds_caminho
            )
            .first()
            is not None
        )