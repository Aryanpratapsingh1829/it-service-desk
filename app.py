"""
app.py
Streamlit web interface for the IT Service Desk system.
Run with:  streamlit run app.py
"""

import matplotlib
matplotlib.use("Agg")          # draw charts without opening a window

import pandas as pd
import streamlit as st

from database import get_connection
from crud import (
    create_ticket, get_all_tickets, get_ticket, search_tickets,
    assign_technician, update_status, delete_ticket,
    VALID_CATEGORIES, VALID_PRIORITIES, VALID_STATUSES,
)
from analysis import load_data, generate_report
from charts import create_all_charts, CHART_DIR

st.set_page_config(page_title="IT Service Desk", page_icon="🛠️", layout="wide")

# Column names in the same order as BASE_SELECT in crud.py
COLUMNS = ["id", "Employee", "Department", "Category", "Description",
           "Priority", "Status", "Created", "Resolved", "Technician"]


def get_lookup(table, id_col, name_col):
    """Return {name: id} for departments or technicians (for dropdowns)."""
    conn = get_connection()
    rows = conn.execute(f"SELECT {name_col}, {id_col} FROM {table}").fetchall()
    conn.close()
    return dict(rows)


def tickets_to_df(rows):
    """Convert ticket rows into a DataFrame with a readable TKT-0001 column."""
    df = pd.DataFrame(rows, columns=COLUMNS)
    df.insert(0, "Ticket", df["id"].apply(lambda x: f"TKT-{x:04d}"))
    return df.drop(columns=["id"])


# ------------------------------------------------------------------
# PAGE 1: Dashboard
# ------------------------------------------------------------------
def page_dashboard():
    st.title("📊 Dashboard")
    df = load_data()
    r = generate_report(df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Tickets", r["total"])
    c2.metric("Resolved", r["resolved"])
    c3.metric("Pending", r["pending"])
    avg = r["avg_hours"]
    c4.metric("Avg Resolution (hrs)", avg if avg is not None else "N/A")

    st.write(f"**Most common issue category:** {r['top_category']}")

    left, right = st.columns(2)
    left.subheader("By Status")
    left.bar_chart(r["by_status"])
    right.subheader("By Priority")
    right.bar_chart(r["by_priority"])

    st.subheader("Latest 5 tickets")
    st.dataframe(tickets_to_df(get_all_tickets()[:5]), hide_index=True)


# ------------------------------------------------------------------
# PAGE 2: Create Ticket
# ------------------------------------------------------------------
def page_create():
    st.title("➕ Create Ticket")
    departments = get_lookup("departments", "department_id", "department_name")

    name = st.text_input("Employee name")
    dept = st.selectbox("Department", list(departments.keys()))
    category = st.selectbox("Issue category", VALID_CATEGORIES)
    priority = st.selectbox("Priority", VALID_PRIORITIES, index=1)
    description = st.text_area("Issue description")

    if st.button("Submit Ticket"):
        try:
            new_id = create_ticket(name, departments[dept], category, description, priority)
            st.success(f"Ticket created: TKT-{new_id:04d}")
        except ValueError as e:
            st.error(str(e))            # validation message from crud.py


# ------------------------------------------------------------------
# PAGE 3: View Tickets
# ------------------------------------------------------------------
def page_view():
    st.title("📋 View Tickets")

    c1, c2, c3 = st.columns(3)
    status = c1.selectbox("Status", ["All"] + VALID_STATUSES)
    category = c2.selectbox("Category", ["All"] + VALID_CATEGORIES)
    priority = c3.selectbox("Priority", ["All"] + VALID_PRIORITIES)
    keyword = st.text_input("Search keyword (name or description)")

    # "All" means no filter, so we pass None
    rows = search_tickets(
        status=None if status == "All" else status,
        category=None if category == "All" else category,
        priority=None if priority == "All" else priority,
        keyword=keyword or None,
    )
    st.write(f"**{len(rows)} tickets found**")
    if rows:
        st.dataframe(tickets_to_df(rows), hide_index=True)


# ------------------------------------------------------------------
# PAGE 4: Update Ticket
# ------------------------------------------------------------------
def page_update():
    st.title("🔧 Update Ticket")
    ids = [r[0] for r in get_all_tickets()]
    if not ids:
        st.info("No tickets available.")
        return

    ticket_id = st.selectbox("Select ticket", ids, format_func=lambda i: f"TKT-{i:04d}")
    ticket = get_ticket(ticket_id)

    st.write(f"**{ticket[1]}** ({ticket[2]}): {ticket[4]}")
    st.write(f"Priority: **{ticket[5]}** | Status: **{ticket[6]}** | "
             f"Technician: **{ticket[9] or 'Not assigned'}**")
    st.divider()

    # --- Assign technician ---
    technicians = get_lookup("technicians", "technician_id", "technician_name")
    tech = st.selectbox("Technician", list(technicians.keys()))
    if st.button("Assign Technician"):
        try:
            assign_technician(ticket_id, technicians[tech])
            st.success("Technician assigned. Reload the page to see the new status.")
        except ValueError as e:
            st.error(str(e))

    # --- Change status ---
    new_status = st.selectbox("New status", VALID_STATUSES)
    if st.button("Update Status"):
        try:
            update_status(ticket_id, new_status)
            st.success(f"Status changed to {new_status}. Reload the page to see it.")
        except ValueError as e:
            st.error(str(e))

    # --- Delete ---
    st.divider()
    confirm = st.checkbox("I confirm I want to delete this ticket")
    if st.button("Delete Ticket") and confirm:
        delete_ticket(ticket_id)
        st.success("Ticket deleted. Reload the page.")


# ------------------------------------------------------------------
# PAGE 5: Reports and Analytics
# ------------------------------------------------------------------
def page_reports():
    st.title("📈 Reports & Analytics")
    df = load_data()
    r = generate_report(df)

    st.write(f"**Total:** {r['total']} | **Resolved:** {r['resolved']} | "
             f"**Pending:** {r['pending']} | **Top category:** {r['top_category']}")

    # Regenerate the 4 Matplotlib charts, then show the saved PNGs
    create_all_charts()
    c1, c2 = st.columns(2)
    c1.image(str(CHART_DIR / "1_status_distribution.png"))
    c2.image(str(CHART_DIR / "2_category_distribution.png"))
    c3, c4 = st.columns(2)
    c3.image(str(CHART_DIR / "3_department_tickets.png"))
    c4.image(str(CHART_DIR / "4_priority_distribution.png"))

    st.download_button("Download all tickets (CSV)",
                       df.to_csv(index=False), "tickets_report.csv", "text/csv")


# ------------------------------------------------------------------
# Sidebar navigation
# ------------------------------------------------------------------
st.sidebar.title("🛠️ IT Service Desk")
page = st.sidebar.radio("Go to", ["Dashboard", "Create Ticket", "View Tickets",
                                  "Update Ticket", "Reports & Analytics"])

if page == "Dashboard":
    page_dashboard()
elif page == "Create Ticket":
    page_create()
elif page == "View Tickets":
    page_view()
elif page == "Update Ticket":
    page_update()
else:
    page_reports()