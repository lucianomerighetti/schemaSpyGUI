# connection_tester.py

import socket
import time
from pathlib import Path

from infrastructure.database.connection_result import (
    ConnectionResult
)

class ConnectionTester:

    def test(self, connection):

        db = connection.database_type.lower()

        if db == "oracle":
            return self._test_oracle(connection)

        if db == "sql server":
            return self._test_sqlserver(connection)

        if db == "postgresql":
            return self._test_postgresql(connection)

        if db == "mysql":
            return self._test_mysql(connection)

        raise ValueError(
            "Banco não suportado."
        )

    @staticmethod
    def test_connection( tp_database: str, nm_host: str, nu_porta: int, ds_caminho: str = "") -> ConnectionResult:

        if tp_database in ("SQLite", "Access"):
            return ConnectionTester.test_file(ds_caminho)

        return ConnectionTester.test_tcp(nm_host, nu_porta)

    @staticmethod
    def test_tcp(host: str, port: int) -> ConnectionResult:

        start = time.time()

        try:
            socket.create_connection((host, port), timeout=5)
            elapsed = int((time.time() - start) * 1000)
            return ConnectionResult( success=True, message=(f"Conexão TCP OK ({elapsed} ms)"), elapsed_ms=elapsed)

        except Exception as ex:
            return ConnectionResult(success=False, message=str(ex))

    @staticmethod
    def test_file(path: str) -> ConnectionResult:
        if not path:
            return ConnectionResult(success=False, message="Arquivo não informado.")

        file = Path(path)

        if not file.exists():
            return ConnectionResult(success=False, message="Arquivo não encontrado.")

        return ConnectionResult(success=True, message="Arquivo localizado.")