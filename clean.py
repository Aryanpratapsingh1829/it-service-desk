from database import get_connection

conn = get_connection()
conn.execute("DELETE FROM tickets")
conn.commit()

count = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
print("Tickets left:", count)

conn.close()