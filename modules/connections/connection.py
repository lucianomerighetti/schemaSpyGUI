# Artefato:  connection.py

from typing import Optional
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

    # BUG FIX: Alteração - Colunas marcadas como nullable=True para suportar diferentes tipos de banco (arquivo/servidor)
    nm_host: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    nu_porta: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )

    nm_database: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    nm_schema: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    nm_usuario: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    tx_password: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    ds_caminho: Mapped[Optional[str]] = mapped_column(
        String(1000),
        nullable=True
    )

    ds_jdbc_driver: Mapped[Optional[str]] = mapped_column(
        String(1000),
        nullable=True
    )

    ds_jdbc_url: Mapped[Optional[str]] = mapped_column(
        String(2000),
        nullable=True
    )

    fl_ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    @property
    def is_file_database(self) -> bool:
        return self.tp_database.lower() in {
            "sqlite",
            "access",
            "firebird_embedded",
            "duckdb"
        }

    @property
    def is_server_database(self) -> bool:
        return not self.is_file_database

    @property
    def is_oracle(self) -> bool:
        return self.tp_database == "Oracle"