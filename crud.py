"""
crud.py
CRUD operations (Create, Read, Update, Delete) for support tickets,
with input validation and error handling.
"""

import sqlite3
from datetime import datetime
from database import get_connection

VALID_CATEGORIES = ["Network", "Software", "Hardware", "Database", "Application"]
VALID_PRIORITIES = ["Low", "Medium", "High", "Critical"]
VALID_STATUSES = ["Open", "In Progress", "Resolved"]


def now():
    """Return the current date-time as text: YYYY-MM-DD HH:MM:SS"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def validate_ticket_input(employee_name, department_id, category, description, priority):
    """
    Check user input BEFORE it reaches the database.
    Raises ValueError with a clear message if something is wrong.
    """
    if not employee_name or not employee_name.strip():
        raise ValueError("Employee name cannot be empty.")
    if not description or len(description.strip()) < 5:
        raise ValueError("Description must be at least 5 characters.")
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Category must be one of {VALID_CATEGORIES}")
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Priority must be one of {VALID_PRIORITIES}")
    if not isinstance(department_id, int):
        raise ValueError("Department ID must be a number.")


# ---------------------------- CREATE ----------------------------
def create_ticket(employee_name, department_id, category, description, priority):
    """Insert a new ticket (status = Open) and return its new ticket_id."""
    validate_ticket_input(employee_name, department_id, category, description, priority)
    conn = get_connection()
    try:
        cursor = conn.execute(
            """INSERT INTO tickets (employee_name, department_id, issue_category,
                                    issue_description, priority, status, created_date)
               VALUES (?, ?, ?, ?, ?, 'Open', ?)""",
            (employee_name.strip(), department_id, category, description.strip(), priority, now()),
        )
        conn.commit()
        return cursor.lastrowid          # the auto-generated ticket_id
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Database rejected the ticket: {e}")
    finally:
        conn.close()


# ----------------------------- READ -----------------------------
# JOIN replaces department_id / technician_id numbers with readable names
BASE_SELECT = """
    SELECT t.ticket_id, t.employee_name, d.department_name, t.issue_category,
           t.issue_description, t.priority, t.status, t.created_date,
           t.resolved_date, tech.technician_name
    FROM tickets t
    JOIN departments d ON t.department_id = d.department_id
    LEFT JOIN technicians tech ON t.technician_id = tech.technician_id
"""


def get_all_tickets():
    """Return all tickets, newest first."""
    conn = get_connection()
    try:
        return conn.execute(BASE_SELECT + " ORDER BY t.created_date DESC").fetchall()
    finally:
        conn.close()


def get_ticket(ticket_id):
    """Return one ticket by ID, or None if it does not exist."""
    conn = get_connection()
    try:
        return conn.execute(BASE_SELECT + " WHERE t.ticket_id = ?", (ticket_id,)).fetchone()
    finally:
        conn.close()


def search_tickets(status=None, category=None, priority=None, keyword=None):
    """
    Filter tickets. Any argument left as None is ignored.
    Example: search_tickets(status='Open', priority='Critical')
    """
    conditions = []
    values = []
    if status:
        conditions.append("t.status = ?")
        values.append(status)
    if category:
        conditions.append("t.issue_category = ?")
        values.append(category)
    if priority:
        conditions.append("t.priority = ?")
        values.append(priority)
    if keyword:
        conditions.append("(t.issue_description LIKE ? OR t.employee_name LIKE ?)")
        values.extend([f"%{keyword}%", f"%{keyword}%"])

    query = BASE_SELECT
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY t.created_date DESC"

    conn = get_connection()
    try:
        return conn.execute(query, values).fetchall()
    finally:
        conn.close()


# ---------------------------- UPDATE ----------------------------
def assign_technician(ticket_id, technician_id):
    """Assign a technician. An Open ticket automatically becomes In Progress."""
    conn = get_connection()
    try:
        ticket = conn.execute("SELECT status FROM tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
        if ticket is None:
            raise ValueError(f"Ticket {ticket_id} not found.")
        new_status = "In Progress" if ticket[0] == "Open" else ticket[0]
        conn.execute(
            "UPDATE tickets SET technician_id = ?, status = ? WHERE ticket_id = ?",
            (technician_id, new_status, ticket_id),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError(f"Technician {technician_id} does not exist.")
    finally:
        conn.close()


def update_status(ticket_id, new_status):
    """
    Change ticket status.
    - Resolved needs an assigned technician and sets resolved_date to now.
    - Any other status clears resolved_date.
    """
    if new_status not in VALID_STATUSES:
        raise ValueError(f"Status must be one of {VALID_STATUSES}")
    conn = get_connection()
    try:
        ticket = conn.execute(
            "SELECT technician_id FROM tickets WHERE ticket_id = ?", (ticket_id,)
        ).fetchone()
        if ticket is None:
            raise ValueError(f"Ticket {ticket_id} not found.")
        if new_status == "Resolved":
            if ticket[0] is None:
                raise ValueError("Assign a technician before resolving the ticket.")
            conn.execute(
                "UPDATE tickets SET status = ?, resolved_date = ? WHERE ticket_id = ?",
                (new_status, now(), ticket_id),
            )
        else:
            conn.execute(
                "UPDATE tickets SET status = ?, resolved_date = NULL WHERE ticket_id = ?",
                (new_status, ticket_id),
            )
        conn.commit()
    finally:
        conn.close()


# ---------------------------- DELETE ----------------------------
def delete_ticket(ticket_id):
    """Delete a ticket. Returns True if deleted, False if it did not exist."""
    conn = get_connection()
    try:
        cursor = conn.execute("DELETE FROM tickets WHERE ticket_id = ?", (ticket_id,))
        conn.commit()
        return cursor.rowcount > 0       # rowcount = how many rows were deleted
    finally:
        conn.close()