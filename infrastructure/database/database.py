# database.py

from pathlib import Path
from sqlalchemy import create_engine

DB_DIR = "data" 
DB_NAME = "schemaspy_gui.db"
DB_PATH = DB_DIR + "/" + DB_NAME
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=False
)