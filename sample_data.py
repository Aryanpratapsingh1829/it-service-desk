"""
sample_data.py
Loads 32 fictional tickets into the tickets table for testing.
Safe to run many times: it clears old tickets first.
"""

from database import get_connection

# Each ticket is a tuple in this order:
# (employee_name, department_id, issue_category, issue_description,
#  priority, status, created_date, resolved_date, technician_id)
#
# department_id: 1=HR, 2=Finance, 3=Sales, 4=Marketing, 5=Operations, 6=Engineering
# technician_id: 1=Rahul(Network), 2=Neha(Software), 3=Arjun(Hardware),
#                4=Pooja(Database), 5=Sanjay(Application)
# None means NULL (empty) in the database.

tickets = [
    # ---------- 20 Resolved tickets ----------
    ("Aarav Sharma", 1, "Network", "Cannot connect to office Wi-Fi", "High", "Resolved", "2026-10-01 09:15:00", "2026-10-01 11:45:00", 1),
    ("Priya Singh", 2, "Software", "Excel crashes when opening large files", "Medium", "Resolved", "2026-10-02 10:00:00", "2026-10-03 12:30:00", 2),
    ("Rohan Gupta", 3, "Hardware", "Laptop battery drains within one hour", "Medium", "Resolved", "2026-10-03 14:20:00", "2026-10-06 16:00:00", 3),
    ("Sneha Patil", 6, "Database", "Unable to connect to the customer database", "Critical", "Resolved", "2026-10-04 08:45:00", "2026-10-04 10:15:00", 4),
    ("Vikram Rao", 5, "Application", "Inventory app shows blank screen after login", "High", "Resolved", "2026-10-05 11:30:00", "2026-10-06 09:30:00", 5),
    ("Ananya Das", 4, "Network", "VPN disconnects every 10 minutes", "High", "Resolved", "2026-10-06 13:00:00", "2026-10-07 10:00:00", 1),
    ("Karan Malhotra", 2, "Software", "Antivirus license expired", "Low", "Resolved", "2026-10-07 09:40:00", "2026-10-07 15:00:00", 2),
    ("Meera Joshi", 1, "Hardware", "Keyboard keys not responding", "Low", "Resolved", "2026-10-08 10:10:00", "2026-10-09 11:00:00", 3),
    ("Aditya Kulkarni", 6, "Application", "HR portal shows error 500 on leave request", "High", "Resolved", "2026-10-09 15:25:00", "2026-10-10 12:00:00", 5),
    ("Kavya Reddy", 3, "Network", "Slow internet on the sales floor", "Medium", "Resolved", "2026-10-10 09:05:00", "2026-10-10 17:30:00", 1),
    ("Nikhil Bansal", 5, "Database", "Monthly report query running very slow", "Medium", "Resolved", "2026-10-12 11:00:00", "2026-10-14 10:30:00", 4),
    ("Isha Verma", 4, "Software", "Cannot install Adobe Photoshop", "Low", "Resolved", "2026-10-13 14:00:00", "2026-10-14 16:45:00", 2),
    ("Manish Tiwari", 2, "Hardware", "Printer not detected by computer", "Medium", "Resolved", "2026-10-14 10:30:00", "2026-10-15 11:15:00", 3),
    ("Divya Menon", 6, "Network", "Cannot access internal Git server", "High", "Resolved", "2026-10-15 09:50:00", "2026-10-15 13:20:00", 1),
    ("Harsh Pandey", 3, "Application", "CRM dashboard not loading data", "Critical", "Resolved", "2026-10-16 08:30:00", "2026-10-16 12:00:00", 5),
    ("Ritu Saxena", 1, "Software", "MS Word keeps freezing while saving", "Medium", "Resolved", "2026-10-19 10:20:00", "2026-10-20 14:00:00", 2),
    ("Siddharth Jain", 5, "Hardware", "Monitor flickering continuously", "Low", "Resolved", "2026-10-20 12:15:00", "2026-10-22 10:00:00", 3),
    ("Pallavi Deshmukh", 2, "Database", "Duplicate records appearing in payroll table", "High", "Resolved", "2026-10-21 09:00:00", "2026-10-22 15:30:00", 4),
    ("Gaurav Chauhan", 4, "Network", "Wi-Fi password not working on new laptop", "Low", "Resolved", "2026-10-22 10:45:00", "2026-10-22 12:00:00", 1),
    ("Neelam Yadav", 6, "Application", "Mobile app crashes on startup", "Critical", "Resolved", "2026-10-26 09:10:00", "2026-10-27 11:00:00", 5),

    # ---------- 6 In Progress tickets (technician assigned, not resolved) ----------
    ("Tanvi Arora", 3, "Software", "Outlook not syncing emails", "Medium", "In Progress", "2026-11-02 10:00:00", None, 2),
    ("Yash Mishra", 5, "Network", "Intermittent LAN failure in warehouse office", "High", "In Progress", "2026-11-03 09:30:00", None, 1),
    ("Simran Kaur", 2, "Database", "Backup job failing every night", "Critical", "In Progress", "2026-11-04 08:15:00", None, 4),
    ("Abhishek Nair", 6, "Hardware", "Desktop restarts randomly", "High", "In Progress", "2026-11-05 11:40:00", None, 3),
    ("Lakshmi Iyer", 1, "Application", "Payroll module gives wrong tax calculation", "High", "In Progress", "2026-11-06 14:10:00", None, 5),
    ("Mohit Sharma", 3, "Software", "Zoom camera not detected", "Low", "In Progress", "2026-11-09 10:25:00", None, 2),

    # ---------- 6 Open tickets (no technician yet) ----------
    ("Pooja Bhatt", 4, "Network", "Cannot access shared drive", "Medium", "Open", "2026-11-09 15:00:00", None, None),
    ("Arjun Kapoor", 6, "Database", "Need access to the analytics database", "Low", "Open", "2026-11-10 09:00:00", None, None),
    ("Shreya Ghosh", 2, "Hardware", "Laptop screen cracked", "Medium", "Open", "2026-11-10 12:30:00", None, None),
    ("Rahul Dubey", 5, "Application", "Attendance app login failing for new employees", "High", "Open", "2026-11-11 09:45:00", None, None),
    ("Aarti Menon", 1, "Software", "Need Python installed for training", "Low", "Open", "2026-11-11 14:20:00", None, None),
    ("Deepak Chopra", 3, "Network", "Entire sales floor has no internet", "Critical", "Open", "2026-11-12 09:05:00", None, None),
]


def load_sample_data():
    """
    Delete old tickets, reset the ID counter, then insert all sample tickets.
    """
    conn = get_connection()
    try:
        # Step 1: remove old tickets
        conn.execute("DELETE FROM tickets")
        # Step 2: restart ticket_id from 1 again
        conn.execute("DELETE FROM sqlite_sequence WHERE name = 'tickets'")

        # Step 3: insert all tickets in one go
        conn.executemany("""
            INSERT INTO tickets (
                employee_name, department_id, issue_category, issue_description,
                priority, status, created_date, resolved_date, technician_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tickets)

        conn.commit()

        count = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
        print(f"{count} tickets loaded successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    load_sample_data()