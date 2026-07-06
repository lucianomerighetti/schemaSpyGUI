# connection.py

from sqlalchemy import (
    Boolean,
    Integer,
    String
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure.database import (
    Base
)

class Connection(Base):

    __tablename__ = "tb_conexao"

    id_conexao: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nm_conexao: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    tp_database: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    nm_host: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    nu_porta: Mapped[int] = mapped_column(
        Integer
    )

    nm_database: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    nm_schema: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    nm_usuario: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    tx_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    ds_caminho: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    ds_jdbc_driver: Mapped[str] = mapped_column(
        String(1000),
        nullable=True
    )

    ds_jdbc_url: Mapped[str] = mapped_column(
        String(2000),
        nullable=True
    )

    fl_ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    @property
    def is_file_database(self) -> bool:
        return self.tp_database in (
            "Access",
            "SQLite"
        )

    @property
    def is_server_database(self) -> bool:
        return not self.is_file_database

    @property
    def is_oracle(self) -> bool:
        return self.tp_database == "Oracle"