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
    Setting,
    Parameter,
    PropertyFile
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

def seed_parameters():
    from infrastructure.database.session import SessionLocal
    from modules.settings.support import Parameter
    
    session = SessionLocal()
    try:
        if session.query(Parameter).count() > 0:
            return
            
        parameters = [
            ("-t", "Database type (e.g. pgsql, mysql, ora, etc.)"),
            ("-dp", "Path to the JDBC driver jar"),
            ("-db", "Name of the database"),
            ("-host", "Host name or IP address of the database server"),
            ("-port", "Port number of the database server"),
            ("-s", "Schema name to explore"),
            ("-u", "Database username"),
            ("-p", "Database password"),
            ("-o", "Output directory"),
            ("-meta", "Path to XML metadata file"),
            ("-desc", "Description to be displayed on summary page"),
            ("-i", "Regular expression of table names to include"),
            ("-I", "Regular expression of table names to exclude"),
            ("-x", "Regular expression of column names to exclude"),
            ("-charset", "Character set used for HTML output"),
            ("-font", "Font name for generated HTML"),
            ("-fontsize", "Font size for generated HTML"),
            ("-css", "Path to custom CSS file"),
            ("-vizjs", "Use embedded Viz.js instead of Graphviz"),
            ("-degree", "Limits degree of separation in diagrams (1 or 2)"),
            ("-noRows", "Don't query or display row counts"),
            ("-rails", "Specifies if it is a Ruby on Rails database"),
            ("-aHTML", "Allow HTML in comments"),
            ("-noHTML", "Don't generate HTML documentation"),
            ("-noLogo", "Don't include the SchemaSpy logo"),
            ("-noAds", "Don't display sponsor ads"),
            ("-dincFK", "Don't query foreign keys"),
            ("-sso", "Single Sign-On")
        ]
        
        for name, desc in parameters:
            param = Parameter(nm_parametro=name, ds_parametro=desc)
            session.add(param)
            
        session.commit()
        print("Migração: Tabela de apoio ta_parametro populada com sucesso.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao popular parâmetros: {e}")
    finally:
        session.close()

seed_parameters()

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
