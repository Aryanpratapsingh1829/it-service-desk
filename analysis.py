"""
analysis.py
Analyses the tickets data using Pandas and prints a report.
"""

import pandas as pd
from database import get_connection


def load_data():
    """
    Read tickets (with department and technician names) into a DataFrame.
    A DataFrame is like an Excel sheet inside Python.
    """
    conn = get_connection()
    query = """
        SELECT t.ticket_id, t.employee_name, d.department_name,
               t.issue_category, t.priority, t.status,
               t.created_date, t.resolved_date, tech.technician_name
        FROM tickets t
        JOIN departments d ON t.department_id = d.department_id
        LEFT JOIN technicians tech ON t.technician_id = tech.technician_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    # Convert text dates to real datetime so we can do date maths
    df["created_date"] = pd.to_datetime(df["created_date"])
    df["resolved_date"] = pd.to_datetime(df["resolved_date"])
    return df


def generate_report(df):
    """Return a dictionary containing all the key numbers."""
    total = len(df)
    resolved = (df["status"] == "Resolved").sum()
    pending = total - resolved

    # Resolution time = resolved_date - created_date (only for resolved tickets)
    resolved_df = df[df["status"] == "Resolved"].copy()
    resolved_df["hours"] = (
        resolved_df["resolved_date"] - resolved_df["created_date"]
    ).dt.total_seconds() / 3600

    return {
        "total": total,
        "resolved": int(resolved),
        "pending": int(pending),
        "top_category": df["issue_category"].value_counts().idxmax(),
        "by_department": df["department_name"].value_counts(),
        "by_priority": df["priority"].value_counts(),
        "by_status": df["status"].value_counts(),
        "by_category": df["issue_category"].value_counts(),
        "avg_hours": round(resolved_df["hours"].mean(), 2) if len(resolved_df) else None,
    }


if __name__ == "__main__":
    df = load_data()
    r = generate_report(df)

    print("===== IT SERVICE DESK REPORT =====")
    print("Total tickets   :", r["total"])
    print("Resolved        :", r["resolved"])
    print("Pending         :", r["pending"])
    print("Top category    :", r["top_category"])
    print("Avg resolution  :", r["avg_hours"], "hours")
    print("\nTickets by department:\n", r["by_department"])
    print("\nTickets by priority:\n", r["by_priority"])
    print("\nTickets by category:\n", r["by_category"])