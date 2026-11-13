from database import get_connection

conn = get_connection()

print("Tickets by status:")
for row in conn.execute("SELECT status, COUNT(*) FROM tickets GROUP BY status"):
    print(" ", row)

print("\nFirst 3 tickets:")
for row in conn.execute("SELECT * FROM tickets LIMIT 3"):
    print(" ", row)

conn.close()