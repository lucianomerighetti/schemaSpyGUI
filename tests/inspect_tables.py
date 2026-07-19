# inspect_tables.py
import sqlite3

def inspect():
    db_path = "e:/Workspace/ws_python/M2DE - Schema Spy GUI/application/platform/frontend/apps/gui/schemaSpyGUI/data/schemaspy_gui_v2.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Tables found: {tables}")
    
    for table in tables:
        if table.startswith("sqlite_"):
            continue
        print(f"\n--- Table: {table} ---")
        
        # Columns
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        print("Columns:")
        for col in columns:
            # col: (cid, name, type, notnull, dflt_value, pk)
            print(f"  - {col[1]} ({col[2]}) {'[PK]' if col[5] else ''}")
            
        # Foreign Keys
        cursor.execute(f"PRAGMA foreign_key_list({table})")
        fkeys = cursor.fetchall()
        if fkeys:
            print("Foreign Keys:")
            for fk in fkeys:
                # fk: (id, seq, table, from, to, on_update, on_delete, match)
                print(f"  - {fk[3]} -> {fk[2]}.{fk[4]} (ON DELETE: {fk[6]})")
                
    conn.close()

if __name__ == '__main__':
    inspect()
