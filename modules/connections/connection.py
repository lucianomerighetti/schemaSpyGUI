# connection.py
from typing import Optional
from sqlalchemy import (
    Boolean,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure.database import (
    Base
)

class Connection(Base):
    __tablename__ = "tb_conexao"

    __table_args__ = (
        UniqueConstraint(
            "NM_CONEXAO", "TP_DATABASE", "NM_HOST", "NU_PORTA",
            "NM_DATABASE", "NM_SCHEMA", "NM_USUARIO", "TX_PASSWORD", "DS_CAMINHO",
            name="uq_tb_conexao_campos"
        ),
    )

    id_conexao: Mapped[int] = mapped_column(
        "ID_CONEXAO",
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_projeto: Mapped[Optional[int]] = mapped_column(
        "ID_PROJETO",
        Integer,
        ForeignKey("tb_projeto.ID_PROJETO", ondelete="CASCADE"),
        nullable=True
    )

    nm_conexao: Mapped[str] = mapped_column(
        "NM_CONEXAO",
        String(100),
        nullable=False
    )

    tp_database: Mapped[str] = mapped_column(
        "TP_DATABASE",
        String(50),
        nullable=False
    )

    nm_host: Mapped[Optional[str]] = mapped_column(
        "NM_HOST",
        String(255),
        nullable=True
    )

    nu_porta: Mapped[Optional[int]] = mapped_column(
        "NU_PORTA",
        Integer,
        nullable=True
    )

    nm_database: Mapped[Optional[str]] = mapped_column(
        "NM_DATABASE",
        String(100),
        nullable=True
    )

    nm_schema: Mapped[Optional[str]] = mapped_column(
        "NM_SCHEMA",
        String(100),
        nullable=True
    )

    nm_usuario: Mapped[Optional[str]] = mapped_column(
        "NM_USUARIO",
        String(100),
        nullable=True
    )

    tx_password: Mapped[Optional[str]] = mapped_column(
        "TX_PASSWORD",
        String(255),
        nullable=True
    )

    ds_caminho: Mapped[Optional[str]] = mapped_column(
        "DS_CAMINHO",
        String(1000),
        nullable=True
    )

    ds_jdbc_driver: Mapped[Optional[str]] = mapped_column(
        "DS_JDBC_DRIVER",
        String(1000),
        nullable=True
    )

    ds_jdbc_url: Mapped[Optional[str]] = mapped_column(
        "DS_JDBC_URL",
        String(2000),
        nullable=True
    )

    fl_ativo: Mapped[bool] = mapped_column(
        "FL_ATIVO",
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