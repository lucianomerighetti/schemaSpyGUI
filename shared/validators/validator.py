# validator.py

import os
import ipaddress
import re
from pathlib import (
    Path
)
from shared.validators.validation_result import (
    ValidationResult
)

class Validator:

    @staticmethod
    def validate(*validators):
        for result in validators:
            if not result.valid:
                return result

        return ValidationResult(True)

    @staticmethod
    def required(value, field_name: str) -> ValidationResult:
        if value is None:
            return ValidationResult(False, f"Informe {field_name}.")
        if isinstance(value, str):
            if not str(value).strip():
                return ValidationResult(False, f"Informe {field_name}.")
        return ValidationResult(True)

    @staticmethod
    def min_length(value, field_name: str, min_size: int) -> ValidationResult:
        value = str(value).strip()

        if len(value) < min_size:
            return ValidationResult(False,f"{field_name} deve possuir no mínimo {min_size} caracteres.")
        
        return ValidationResult(True)

    @staticmethod
    def max_length(value, field_name: str, max_size: int) -> ValidationResult:
        value = str(value).strip()
        
        if len(value) > max_size:
            return ValidationResult(False,f"{field_name} deve possuir no máximo {max_size} caracteres.")
        
        return ValidationResult(True)

    @staticmethod
    def integer(value, field_name: str) -> ValidationResult:
        try:
            int(value)
            return ValidationResult(True)
        except (TypeError, ValueError):
            return ValidationResult(False, f"{field_name} deve ser um número inteiro.")

    @staticmethod
    def port(value) -> ValidationResult:
        try:
            port = int(value)
        except (TypeError, ValueError):
            return ValidationResult(False, "Porta inválida.")

        if port < 1 or port > 65535:
            return ValidationResult(False, "Porta deve estar entre 1 e 65535.")

        return ValidationResult(True)

    @staticmethod
    def ip(value) -> ValidationResult:
        try:
            ipaddress.ip_address(str(value).strip())
            return ValidationResult(True)
        except ValueError:
            return ValidationResult(False, "Endereço IP inválido.")

    @staticmethod
    def database_name(value) -> ValidationResult:
        value = str(value).strip()
        if not value:
            return ValidationResult(False, "Informe o nome do banco.")

        pattern = r"^[a-zA-Z0-9_\-$]+$"
        if not re.match(pattern, value):
            return ValidationResult(False, "Nome do banco contém caracteres inválidos.")

        return ValidationResult(True)
    
    @staticmethod
    def hostname(value) -> ValidationResult:
        value = str(value).strip()
        if not value:
            return ValidationResult(False,"Informe o Host.")
        pattern = (
            r"^(([a-zA-Z0-9]"
            r"([a-zA-Z0-9\-]{0,61}"
            r"[a-zA-Z0-9])?)"
            r"(\.[a-zA-Z0-9]"
            r"([a-zA-Z0-9\-]{0,61}"
            r"[a-zA-Z0-9])?)*)$"
        )

        if not re.match(pattern, value):
            return ValidationResult(False, "Hostname inválido.")
        return ValidationResult(True)
    
    @staticmethod
    def jdbc_driver(value) -> ValidationResult:
        value = str(value).strip()
        if not value:
            return ValidationResult(False, "Informe o Driver JDBC.")

        if not value.lower().endswith(".jar"):
            return ValidationResult(False, "Driver JDBC deve ser um arquivo .jar.")

        return ValidationResult(True)

    @staticmethod
    def schema_name(value) -> ValidationResult:
        value = str(value).strip()
        if not value:
            return ValidationResult(False, "Informe o Schema.")

        pattern = r"^[a-zA-Z0-9_\-$]+$"

        if not re.match(pattern, value):
            return ValidationResult(False, "Schema inválido.")
        return ValidationResult(True)

    @staticmethod
    def username(value) -> ValidationResult:
        value = str(value).strip()
        if not value:
            return ValidationResult(False, "Informe o Usuário.")

        if len(value) < 2:
            return ValidationResult(False, "Usuário inválido.")

        return ValidationResult(True)
    
    @staticmethod
    def password(value) -> ValidationResult:
        if value is None:
            return ValidationResult(False, "Informe a Senha.")

        value = str(value)

        if not value.strip():
            return ValidationResult(False, "Informe a Senha.")

        return ValidationResult(True)

    @staticmethod
    def file_exists(file_path) -> ValidationResult:
        path = Path(str(file_path))
        if not path.exists():
            return ValidationResult(False, f"Arquivo não encontrado: {path}")

        if not path.is_file():
            return ValidationResult(False, f"Não é um arquivo válido: {path}")

        return ValidationResult(True)

    @staticmethod
    def directory_exists(directory) -> ValidationResult:
        path = Path(str(directory))
        if not path.exists():
            return ValidationResult(False, f"Diretório não encontrado: {path}")

        if not path.is_dir():
            return ValidationResult(False, f"Diretório inválido: {path}")

        return ValidationResult(True)

    @staticmethod
    def jar_file(file_path) -> ValidationResult:
        result = Validator.file_exists(file_path)
        if not result.valid:
            return result

        if not str(file_path).lower().endswith(".jar"):
            return ValidationResult(False, "Arquivo deve possuir extensão .jar.")

        return ValidationResult(True)
    
    @staticmethod
    def oracle_sid(value) -> ValidationResult:
        value = str(value).strip()
        if not value:
            return ValidationResult(False, "Informe o SID Oracle.")
        
        pattern = r"^[a-zA-Z0-9_]+$"
        
        if not re.match(pattern, value):
            return ValidationResult( False, "SID Oracle inválido.")
        
        return ValidationResult(True)

    @staticmethod
    def oracle_service(value) -> ValidationResult:
        value = str(value).strip()

        if not value:
            return ValidationResult(False, "Informe o Service Name.")

        pattern = r"^[a-zA-Z0-9._-]+$"

        if not re.match(pattern, value):
            return ValidationResult(False, "Service Name inválido.")

        return ValidationResult(True)

    @staticmethod
    def jdbc_url(value) -> ValidationResult:
        value = str(value).strip()

        if not value:
            return ValidationResult(False, "Informe a JDBC URL.")

        if not value.startswith("jdbc:"):
            return ValidationResult(False, "JDBC URL inválida.")

        return ValidationResult(True)

    @staticmethod
    def java_home(value) -> ValidationResult:
        result = Validator.directory_exists(value)
        
        if not result.valid:
            return result

        java_path = (Path(value) / "bin")

        if not java_path.exists():
            return ValidationResult(False, "Diretório Java inválido.")

        return ValidationResult(True)

    @staticmethod
    def java_executable(value) -> ValidationResult:
        result = Validator.file_exists(value)

        if not result.valid:
            return result

        filename = Path(value).name.lower()
        
        if filename not in ("java.exe", "java"):
            return ValidationResult(False, "Executável Java inválido.")

        return ValidationResult(True)

    @staticmethod
    def schemaspy_jar(value) -> ValidationResult:
        result = Validator.jar_file(value)

        if not result.valid:
            return result

        filename = (Path(value).name.lower())

        if "schemaspy" not in filename:
            return ValidationResult(False, "Arquivo SchemaSpy inválido.")

        return ValidationResult(True)

    @staticmethod
    def output_directory(value) -> ValidationResult:
        return Validator.directory_exists(value)

    @staticmethod
    def connection_name(value) -> ValidationResult:
        result = Validator.required(value, "o Nome da Conexão")

        if not result.valid:
            return result

        return Validator.max_length(value, 100, "Nome da Conexão")

    @staticmethod
    def project_name(value) -> ValidationResult:
        result = Validator.required(value, "o Nome do Projeto")

        if not result.valid:
            return result

        return Validator.max_length(value, 100, "Nome do Projeto")