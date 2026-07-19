# scratch/inspect_db_connections.py
import sqlite3

conn = sqlite3.connect("data/schemaspy_gui.db")
cursor = conn.cursor()

print("--- Projetos ---")
cursor.execute("SELECT id_projeto, nm_projeto FROM tb_projeto")
for r in cursor.fetchall():
    print(r)

print("\n--- Conexões ---")
cursor.execute("SELECT id_conexao, id_projeto, nm_conexao, tp_database FROM tb_conexao")
for r in cursor.fetchall():
    print(r)

conn.close()
