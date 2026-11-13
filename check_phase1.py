from database import get_connection

conn = get_connection()

print("Tables in database:")
for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print(" -", row[0])

print("\nDepartments:")
for row in conn.execute("SELECT * FROM departments"):
    print(" ", row)

print("\nTechnicians:")
for row in conn.execute("SELECT * FROM technicians"):
    print(" ", row)

# ---- Task 1: ek valid ticket daalo ----
conn.execute("""
    INSERT INTO tickets (employee_name, department_id, issue_category,
                         issue_description, priority, created_date)
    VALUES (?, ?, ?, ?, ?, ?)
""", ("Aarav Sharma", 99, "Network", "Cannot connect to office Wi-Fi",
      "High", "2026-11-12 10:30:00"))
conn.commit()

print("\nTickets:")
for row in conn.execute("SELECT * FROM tickets"):
    print(" ", row)

conn.close()