# Artefato:  connection_dto.py

from __future__ import annotations
from dataclasses import (
     dataclass,
     field
)
from datetime import datetime
from typing import Optional

@dataclass(slots=True)
class ConnectionDTO:
    #DTO utilizado pelo módulo de conexões.

    # Identificação
    id_conexao: Optional[int] = None
    # BUG FIX: Implementação - Adicionando id_projeto para relacionamento no DTO
    id_projeto: Optional[int] = None
    nm_conexao: str = ""
    ds_conexao: str = ""
    # Banco
    tp_database: str = ""
    nm_host:     str = ""
    nu_porta:    Optional[int] = None
    nm_database: str = ""
    nm_schema:   str = ""
    nm_usuario:  str = ""
    tx_password: str = ""
    # Bancos baseados em arquivo
    ds_caminho: str = ""
    # Driver
    ds_driver:         str = ""
    ds_jdbc_driver:    str = ""
    ds_jdbc_url:       str = ""
    ds_sqlalchemy_url: str = ""
    # Configurações
    fl_ssl: bool = False
    nu_timeout:    int = 30
    ds_charset:    str = "UTF-8"
    ds_encoding:   str = "UTF-8"
    ds_parametros: str = ""
    # Java / SchemaSpy
    ds_java_home:     str = ""
    ds_schemaspy_jar: str = ""
    # Controle
    fl_ativo:         bool = True
    fl_favorito:      bool = False
    dt_ultimo_acesso: Optional[datetime] = None
    dt_criacao:       datetime = field(default_factory=datetime.now)
    dt_alteracao:     datetime = field(default_factory=datetime.now)

    # Auxiliares
    @property
    def is_new(self) -> bool:
        # Indica se o registro ainda não foi salvo.
        return self.id_conexao is None

    @property
    def is_file_database(self) -> bool:
        # Bancos que utilizam arquivo físico.
        return self.tp_database.lower() in {
            "sqlite",
            "access",
            "firebird_embedded",
            "duckdb",
        }

    @property
    def is_server_database(self) -> bool:
        # Bancos cliente/servidor.
        return not self.is_file_database

    def touch(self) -> None:
        # Atualiza a data da última alteração.
        self.dt_alteracao = datetime.now()

    def clear_password(self) -> None:
        # Remove a senha da memória.
        self.tx_password = ""

    def clone(self) -> "ConnectionDTO":
        # Retorna uma cópia do DTO.
        from copy import deepcopy
        return deepcopy(self)