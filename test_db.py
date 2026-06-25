
from app.database.sqlite import get_connection

conn = get_connection()
cursor = conn.cursor()

queries = [
    ("Available = 1", "SELECT COUNT(*) FROM doctor_records WHERE is_available = 1"),
    ("Available = 'True'", "SELECT COUNT(*) FROM doctor_records WHERE is_available = 'True'"),
    ("Available = TRUE", "SELECT COUNT(*) FROM doctor_records WHERE is_available = TRUE"),
]

for title, query in queries:
    cursor.execute(query)
    print(f"{title}: {cursor.fetchone()[0]}")

conn.close()