from database import get_connection


def run(title, query):
    """Run one SQL query and print the result neatly."""
    conn = get_connection()
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    # Column names from the query result
    columns = [col[0] for col in cursor.description]

    print(f"\n=== {title} ===")
    print(" | ".join(columns))
    for row in rows:
        print(" | ".join(str(v) for v in row))
    print(f"({len(rows)} rows)")
    conn.close()


# ----- Queries go below this line -----

run("1. SELECT all columns (first 5)", """
    SELECT * FROM tickets LIMIT 5
""")
run("2. SELECT specific columns", """
    SELECT employee_name, priority FROM tickets
""")

run("3. WHERE: only Critical tickets", """
    SELECT ticket_id, employee_name, issue_description
    FROM tickets
    WHERE priority = 'Critical'
""")

run("4. ORDER BY: newest first", """
    SELECT ticket_id, employee_name, created_date
    FROM tickets
    ORDER BY created_date DESC
""")