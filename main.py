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

            # --- Migrações de tb_configuracao ---
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tb_configuracao'")
            if cursor.fetchone():
                cursor.execute("PRAGMA table_info(tb_configuracao)")
                columns = [col[1].lower() for col in cursor.fetchall()]
                
                migrations = [
                    ("DS_SCHEMAS_LIST", "ALTER TABLE tb_configuracao ADD COLUMN DS_SCHEMAS_LIST VARCHAR(1000)"),
                    ("DS_CATALOG_FILTER", "ALTER TABLE tb_configuracao ADD COLUMN DS_CATALOG_FILTER VARCHAR(255)"),
                    ("NM_RENDERER", "ALTER TABLE tb_configuracao ADD COLUMN NM_RENDERER VARCHAR(100)"),
                    ("CD_IMAGE_FORMAT", "ALTER TABLE tb_configuracao ADD COLUMN CD_IMAGE_FORMAT VARCHAR(50)"),
                    ("NR_DEGREE_OF_SEPARATION", "ALTER TABLE tb_configuracao ADD COLUMN NR_DEGREE_OF_SEPARATION INTEGER"),
                    ("DS_GRAPHVIZ_PATH", "ALTER TABLE tb_configuracao ADD COLUMN DS_GRAPHVIZ_PATH VARCHAR(1000)"),
                    ("DS_CONNECTION_PROPERTIES", "ALTER TABLE tb_configuracao ADD COLUMN DS_CONNECTION_PROPERTIES VARCHAR(1000)"),
                    ("CD_LANGUAGE", "ALTER TABLE tb_configuracao ADD COLUMN CD_LANGUAGE VARCHAR(50)"),
                    ("FL_VERBOSE", "ALTER TABLE tb_configuracao ADD COLUMN FL_VERBOSE BOOLEAN DEFAULT 0"),
                    ("FL_QUIET", "ALTER TABLE tb_configuracao ADD COLUMN FL_QUIET BOOLEAN DEFAULT 0"),
                    ("DS_POST_PROCESSING", "ALTER TABLE tb_configuracao ADD COLUMN DS_POST_PROCESSING VARCHAR(1000)"),
                    ("FL_PROMPT_PASSWORD", "ALTER TABLE tb_configuracao ADD COLUMN FL_PROMPT_PASSWORD BOOLEAN DEFAULT 0"),
                    ("FL_VIZJS", "ALTER TABLE tb_configuracao ADD COLUMN FL_VIZJS BOOLEAN DEFAULT 0")
                ]
                
                for col_name, sql in migrations:
                    if col_name.lower() not in columns:
                        cursor.execute(sql)
                        conn.commit()
                        print(f"Migração: Coluna {col_name} adicionada em tb_configuracao.")

            # --- Migrações de ta_parametro ---
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ta_parametro'")
            if cursor.fetchone():
                cursor.execute("PRAGMA table_info(ta_parametro)")
                columns = [col[1].lower() for col in cursor.fetchall()]
                
                # 1. Renomear NM_CAMPO_CONFIGURACAO para NM_CAMPO
                if "nm_campo_configuracao" in columns and "nm_campo" not in columns:
                    cursor.execute("ALTER TABLE ta_parametro RENAME COLUMN NM_CAMPO_CONFIGURACAO TO NM_CAMPO")
                    conn.commit()
                    print("Migração: Coluna NM_CAMPO_CONFIGURACAO renomeada para NM_CAMPO em ta_parametro.")
                
                # Recarregar as colunas após o rename
                cursor.execute("PRAGMA table_info(ta_parametro)")
                columns = [col[1].lower() for col in cursor.fetchall()]
                
                # 2. Inserir NM_TABELA se não existir
                if "nm_tabela" not in columns:
                    cursor.execute("ALTER TABLE ta_parametro ADD COLUMN NM_TABELA VARCHAR(100)")
                    conn.commit()
                    print("Migração: Coluna NM_TABELA adicionada em ta_parametro.")
                
                # 3. Criar NM_CAMPO se não existia nenhuma das duas
                if "nm_campo" not in columns and "nm_campo_configuracao" not in columns:
                    cursor.execute("ALTER TABLE ta_parametro ADD COLUMN NM_CAMPO VARCHAR(100)")
                    conn.commit()
                    print("Migração: Coluna NM_CAMPO adicionada em ta_parametro.")
                
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
            ("-t", "Database type (e.g. pgsql, mysql, ora, etc.)", "TP_DATABASE"),
            ("-dp", "Path to the JDBC driver jar", "DS_DRIVER_PATH"),
            ("-db", "Name of the database", "NM_DATABASE"),
            ("-host", "Host name or IP address of the database server", "NM_HOST"),
            ("-port", "Port number of the database server", "NU_PORTA"),
            ("-s", "Schema name to explore", "DS_SCHEMA_EXPLORE"),
            ("-u", "Database username", "NM_USUARIO"),
            ("-p", "Database password", "TX_PASSWORD"),
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
            ("-vizjs", "Use embedded Viz.js instead of Graphviz", "FL_VIZJS"),
            ("-degree", "Limits degree of separation in diagrams (1 or 2)", "NR_DEGREE_OF_SEPARATION"),
            ("-noRows", "Don't query or display row counts", "FL_NO_ROWS"),
            ("-rails", "Specifies if it is a Ruby on Rails database", "FL_RAILS"),
            ("-aHTML", "Allow HTML in comments", "FL_A_HTML"),
            ("-noHTML", "Don't generate HTML documentation", "FL_NO_HTML"),
            ("-noLogo", "Don't include the SchemaSpy logo", "FL_NO_LOGO"),
            ("-noAds", "Don't display sponsor ads", "FL_NO_ADS"),
            ("-dincFK", "Don't query foreign keys", "FL_DINC_FK"),
            ("-sso", "Single Sign-On", "FL_SINGLE_SIGN_ON"),
            ("-schemas", "Comma-separated list of schemas to analyze", "DS_SCHEMAS_LIST"),
            ("-catalog", "Catalog name to filter analysis", "DS_CATALOG_FILTER"),
            ("-renderer", "Graphviz renderer engine (e.g. :cairo)", "NM_RENDERER"),
            ("-imageformat", "Output diagram image format (e.g. svg, png)", "CD_IMAGE_FORMAT"),
            ("-g", "Path to Graphviz installation directory", "DS_GRAPHVIZ_PATH"),
            ("-connprops", "Connection properties as key1=val1;key2=val2", "DS_CONNECTION_PROPERTIES"),
            ("-lang", "Language code for the report (e.g. pt-br)", "CD_LANGUAGE"),
            ("-v", "Verbose execution output", "FL_VERBOSE"),
            ("-q", "Quiet mode - suppresses output", "FL_QUIET"),
            ("-post", "Post-processing command script", "DS_POST_PROCESSING"),
            ("-prompt", "Prompt database password on execution", "FL_PROMPT_PASSWORD")
        ]
        
        for name, desc, col_name in parameters:
            # Determinar a qual tabela o campo pertence
            tab_name = "tb_configuracao"
            if col_name in ["TP_DATABASE", "NM_DATABASE", "NM_HOST", "NU_PORTA", "NM_USUARIO", "TX_PASSWORD"]:
                tab_name = "tb_conexao"
                
            param = session.query(Parameter).filter(Parameter.nm_parametro == name).first()
            if param:
                param.nm_tabela = tab_name
                param.nm_campo = col_name
            else:
                param = Parameter(nm_parametro=name, ds_parametro=desc, nm_tabela=tab_name, nm_campo=col_name)
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
