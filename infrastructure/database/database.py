# database.py

from pathlib import Path
from sqlalchemy import create_engine

DB_DIR = "data" 
DB_NAME = "schemaspy_gui.db"
DB_PATH = DB_DIR + "/" + DB_NAME
DATABASE_URL = f"sqlite:///{DB_PATH}"

# BUG FIX Criação dinâmica do diretório de dados para evitar falhas ao iniciar se a pasta estiver ausente. Código antes da correção: (não havia verificação/criação do diretório data)
Path(DB_DIR).mkdir(parents=True, exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    echo=False
)

# Melhoria de desempenho: ativação do modo WAL no SQLite para otimizar acessos concorrentes e velocidade de gravação
from sqlalchemy import event
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()