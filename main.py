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

            # --- Migrações de ta_parametro ---
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ta_parametro'")
            if cursor.fetchone():
                cursor.execute("PRAGMA table_info(ta_parametro)")
                columns = [col[1].lower() for col in cursor.fetchall()]
                if "nm_campo_configuracao" not in columns:
                    cursor.execute("ALTER TABLE ta_parametro ADD COLUMN NM_CAMPO_CONFIGURACAO VARCHAR(100)")
                    conn.commit()
                    print("Migração: Coluna NM_CAMPO_CONFIGURACAO adicionada em ta_parametro.")
                
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
        parameters = [
            ("-t", "Database type (e.g. pgsql, mysql, ora, etc.)", None),
            ("-dp", "Path to the JDBC driver jar", "DS_DRIVER_PATH"),
            ("-db", "Name of the database", None),
            ("-host", "Host name or IP address of the database server", None),
            ("-port", "Port number of the database server", None),
            ("-s", "Schema name to explore", "DS_SCHEMA_EXPLORE"),
            ("-u", "Database username", None),
            ("-p", "Database password", None),
            ("-o", "Output directory", "DS_OUTPUT_DIR"),
            ("-meta", "Path to XML metadata file", "DS_META_FILE_PATH"),
            ("-desc", "Description to be displayed on summary page", "DE_DESCRIPTION"),
            ("-i", "Regular expression of table names to include", "DS_TABLE_NAME_REGEX"),
            ("-I", "Regular expression of table names to exclude", "DS_TABLE_EXCLUSION_REGEX"),
            ("-x", "Regular expression of column names to exclude", "DS_COLUMN_EXCLUSION_REGEX"),
            ("-charset", "Character set used for HTML output", "CD_CHARSET"),
            ("-font", "Font name for generated HTML", "NM_FONT"),
            ("-fontsize", "Font size for generated HTML", "NR_FONT_SIZE"),
            ("-css", "Path to custom CSS file", "DS_CSS_PATH"),
            ("-vizjs", "Use embedded Viz.js instead of Graphviz", None),
            ("-degree", "Limits degree of separation in diagrams (1 or 2)", None),
            ("-noRows", "Don't query or display row counts", "FL_NO_ROWS"),
            ("-rails", "Specifies if it is a Ruby on Rails database", "FL_RAILS"),
            ("-aHTML", "Allow HTML in comments", "FL_A_HTML"),
            ("-noHTML", "Don't generate HTML documentation", "FL_NO_HTML"),
            ("-noLogo", "Don't include the SchemaSpy logo", "FL_NO_LOGO"),
            ("-noAds", "Don't display sponsor ads", "FL_NO_ADS"),
            ("-dincFK", "Don't query foreign keys", "FL_DINC_FK"),
            ("-sso", "Single Sign-On", "FL_SINGLE_SIGN_ON")
        ]
        
        for name, desc, col_name in parameters:
            param = session.query(Parameter).filter(Parameter.nm_parametro == name).first()
            if param:
                param.nm_campo_configuracao = col_name
            else:
                param = Parameter(nm_parametro=name, ds_parametro=desc, nm_campo_configuracao=col_name)
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
