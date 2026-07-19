# main.py
import sys
from PyQt6.QtWidgets               import QApplication
from shared.components.main_window import MainWindow
from shared.themes.theme_manager   import ThemeManager

from infrastructure.database import (
    Base,
    engine
)
from modules.projects import (
    Project
)
from modules.connections import (
    Connection
)
from modules.settings import (
    Setting
)
from PyQt6.QtGui import QIcon
from infrastructure.database.database import DB_PATH
import sqlite3
import os

# BUG FIX: Implementação - Migrações automáticas de banco de dados para relacionamento e chaves únicas
def run_migrations():
    try:
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # --- Migrações de tb_conexao ---
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tb_conexao'")
            if cursor.fetchone():
                cursor.execute("PRAGMA table_info(tb_conexao)")
                columns = [col[1].lower() for col in cursor.fetchall()]
                if "id_projeto" not in columns:
                    cursor.execute("ALTER TABLE tb_conexao ADD COLUMN id_projeto INTEGER REFERENCES tb_projeto(id_projeto)")
                    conn.commit()
                    print("Migração: Coluna id_projeto adicionada em tb_conexao.")
                
                # Criar índice único composto em tb_conexao
                cursor.execute("""
                    CREATE UNIQUE INDEX IF NOT EXISTS uq_tb_conexao_campos ON tb_conexao(
                        nm_conexao, tp_database, nm_host, nu_porta, 
                        nm_database, nm_schema, nm_usuario, tx_password, ds_caminho
                    )
                """)
                conn.commit()
            
            # --- Migrações de tb_projeto ---
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tb_projeto'")
            if cursor.fetchone():
                cursor.execute("PRAGMA table_info(tb_projeto)")
                columns = [col[1].lower() for col in cursor.fetchall()]
                if "nm_database" not in columns:
                    cursor.execute("ALTER TABLE tb_projeto ADD COLUMN nm_database VARCHAR(100)")
                    conn.commit()
                    print("Migração: Coluna nm_database adicionada em tb_projeto.")
                
                # Criar índice único em nm_projeto de tb_projeto
                cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_nm_projeto ON tb_projeto(nm_projeto)")
                conn.commit()
                
            conn.close()
    except Exception as e:
        print(f"Erro ao rodar migrações: {e}")

run_migrations()
Base.metadata.create_all(bind=engine)

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(
        QIcon("resources/icons/schemaspygui.ico")
        )
    #app.setStyleSheet(ThemeManager.light())
    app.setStyleSheet(ThemeManager.dark())
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
