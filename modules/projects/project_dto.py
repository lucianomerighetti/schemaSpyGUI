# Artefato:  project_dto.py
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass(slots=True)
class ProjectDTO:
    """DTO utilizado pelo módulo de projetos."""

    id_projeto: Optional[int] = None
    nm_projeto: str = ""
    tp_database: str = ""
    # BUG FIX: Implementação - Adicionando propriedade nm_database no DTO do projeto
    nm_database: str = ""
    nm_host: str = ""
    nm_schema: str = ""
    nu_porta: Optional[int] = None
    dt_criacao: datetime = field(default_factory=datetime.now)
    dt_alteracao: datetime = field(default_factory=datetime.now)

    @property
    def is_new(self) -> bool:
        return self.id_projeto is None

    @property
    def is_file_database(self) -> bool:
        return self.tp_database.lower() in {
            "sqlite",
            "access",
            "firebird_embedded",
            "duckdb",
        }

    @property
    def is_server_database(self) -> bool:
        return not self.is_file_database

    def touch(self) -> None:
        self.dt_alteracao = datetime.now()
