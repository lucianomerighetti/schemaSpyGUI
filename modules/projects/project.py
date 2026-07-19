# Artefato:  project.py

from typing import Optional
from sqlalchemy import (
    Integer,
    String
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure.database import (
    Base
)

class Project(Base):

    __tablename__ = "tb_projeto"

    id_projeto: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nm_projeto: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    tp_database: Mapped[str] = mapped_column(
        String(50)
    )

    # BUG FIX: Implementação - Adicionando nm_database em tb_projeto
    nm_database: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    nm_host: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    nm_schema: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    
    nu_porta: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )

    # BUG FIX: Implementação - Propriedades lógicas para obter o tipo de banco de dados (equivalente ao Connection)
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