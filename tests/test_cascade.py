# test_cascade.py
import sys
sys.path.append("e:/Workspace/ws_python/M2DE - Schema Spy GUI/application/platform/frontend/apps/gui/schemaSpyGUI")

from infrastructure.database import SessionLocal
from modules.projects.project import Project
from modules.connections.connection import Connection
from modules.settings.setting import Setting

def run_test():
    session = SessionLocal()
    
    # Clean up
    session.query(Setting).delete()
    session.query(Connection).delete()
    session.query(Project).delete()
    session.commit()
    
    # Create project
    proj = Project(nm_projeto="Test Project", tp_database="SQLite")
    session.add(proj)
    session.commit()
    print(f"Created Project with ID: {proj.id_projeto}")
    
    # Create connection
    conn = Connection(id_projeto=proj.id_projeto, nm_conexao="Test Connection", tp_database="SQLite")
    session.add(conn)
    session.commit()
    print(f"Created Connection with ID: {conn.id_conexao}")
    
    # Create setting
    sett = Setting(id_conexao=conn.id_conexao, nm_setting="Test Setting")
    session.add(sett)
    session.commit()
    print(f"Created Setting with ID: {sett.id_setting}")
    
    # Check counts before delete
    print(f"Projects count before delete: {session.query(Project).count()}")
    print(f"Connections count before delete: {session.query(Connection).count()}")
    print(f"Settings count before delete: {session.query(Setting).count()}")
    
    # Delete project
    print("\nDeleting project...")
    session.delete(proj)
    session.commit()
    
    # Check counts after delete
    print(f"Projects count after delete: {session.query(Project).count()}")
    print(f"Connections count after delete: {session.query(Connection).count()}")
    print(f"Settings count after delete: {session.query(Setting).count()}")
    
    session.close()

if __name__ == '__main__':
    run_test()
