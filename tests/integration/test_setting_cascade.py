# test_setting_cascade.py
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from infrastructure.database import Base
from modules.projects.project import Project
from modules.connections.connection import Connection
from modules.settings.setting import Setting

@pytest.fixture
def db_session():
    # Usar banco SQLite em memória com chaves estrangeiras ativadas
    engine = create_engine("sqlite:///:memory:")
    
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
        
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_database_level_cascade_delete(db_session):
    # 1. Criar projeto
    proj = Project(nm_projeto="Test Project", tp_database="SQLite")
    db_session.add(proj)
    db_session.commit()
    
    # 2. Criar conexão vinculada ao projeto
    conn = Connection(id_projeto=proj.id_projeto, nm_conexao="Test Connection", tp_database="SQLite")
    db_session.add(conn)
    db_session.commit()
    
    # 3. Criar configuração vinculada à conexão
    sett = Setting(id_conexao=conn.id_conexao, nm_setting="Test Setting")
    db_session.add(sett)
    db_session.commit()
    
    # Verificar inserções
    assert db_session.query(Project).count() == 1
    assert db_session.query(Connection).count() == 1
    assert db_session.query(Setting).count() == 1
    
    # 4. Deletar projeto
    db_session.delete(proj)
    db_session.commit()
    
    # Verificar exclusão em cascata em todos os níveis
    assert db_session.query(Project).count() == 0
    assert db_session.query(Connection).count() == 0
    assert db_session.query(Setting).count() == 0

def test_project_controller_count_queries(db_session):
    proj = Project(nm_projeto="P1", tp_database="SQLite")
    db_session.add(proj)
    db_session.commit()
    
    conn = Connection(id_projeto=proj.id_projeto, nm_conexao="C1", tp_database="SQLite")
    db_session.add(conn)
    db_session.commit()
    
    sett = Setting(id_conexao=conn.id_conexao, nm_setting="S1")
    db_session.add(sett)
    db_session.commit()
    
    # Executar as mesmas queries do ProjectController
    n_connections = db_session.query(Connection).filter(Connection.id_projeto == proj.id_projeto).count()
    n_settings = db_session.query(Setting).join(Connection).filter(Connection.id_projeto == proj.id_projeto).count()
    
    assert n_connections == 1
    assert n_settings == 1
