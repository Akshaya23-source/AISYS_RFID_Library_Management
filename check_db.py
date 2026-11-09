from app.db import get_db_connection

conn = get_db_connection()

tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()

print("Database tables:")

for table in tables:
    print(table["name"])

conn.close()