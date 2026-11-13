"""
database.py
Handles the SQLite connection and creates the tables for the
IT Service Desk & Incident Management System.
"""

import sqlite3
from pathlib import Path

# Store the database file next to this script, no matter where we run from
DB_PATH = Path(__file__).parent / "service_desk.db"


def get_connection():
    """
    Open a connection to the SQLite database and return it.
    Every other file will call this function when it needs the database.
    """
    conn = sqlite3.connect(DB_PATH)
    # SQLite ignores foreign keys unless we switch this on for each connection
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    """
    Create the three tables if they don't already exist.
    'IF NOT EXISTS' makes it safe to run this function many times.
    """
    conn = get_connection()
    try:
        conn.executescript("""
            -- Lookup table 1: departments
            CREATE TABLE IF NOT EXISTS departments (
                department_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                department_name TEXT NOT NULL UNIQUE
            );

            -- Lookup table 2: technicians who resolve tickets
            CREATE TABLE IF NOT EXISTS technicians (
                technician_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                technician_name TEXT NOT NULL UNIQUE,
                specialization  TEXT NOT NULL
            );

            -- Main table: support tickets
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_name     TEXT NOT NULL,
                department_id     INTEGER NOT NULL,
                issue_category    TEXT NOT NULL
                    CHECK (issue_category IN
                        ('Network','Software','Hardware','Database','Application')),
                issue_description TEXT NOT NULL,
                priority          TEXT NOT NULL
                    CHECK (priority IN ('Low','Medium','High','Critical')),
                status            TEXT NOT NULL DEFAULT 'Open'
                    CHECK (status IN ('Open','In Progress','Resolved')),
                created_date      TEXT NOT NULL,   -- format: YYYY-MM-DD HH:MM:SS
                resolved_date     TEXT,            -- NULL until the ticket is resolved
                technician_id     INTEGER,         -- NULL until a technician is assigned
                FOREIGN KEY (department_id) REFERENCES departments (department_id),
                FOREIGN KEY (technician_id) REFERENCES technicians (technician_id)
            );
        """)
        conn.commit()
        print("Tables created successfully.")
    finally:
        conn.close()


def insert_lookup_data():
    """
    Fill the departments and technicians tables with fictional starting data.
    'INSERT OR IGNORE' skips rows that already exist (because of UNIQUE),
    so running this twice will not create duplicates.
    """
    departments = [
        ("Human Resources",), ("Finance",), ("Sales",),
        ("Marketing",), ("Operations",), ("Engineering",),
    ]
    technicians = [
        ("Rahul Verma",   "Network"),
        ("Neha Kapoor",   "Software"),
        ("Arjun Mehta",   "Hardware"),
        ("Pooja Nair",    "Database"),
        ("Sanjay Iyer",   "Application"),
    ]

    conn = get_connection()
    try:
        conn.executemany(
            "INSERT OR IGNORE INTO departments (department_name) VALUES (?)",
            departments,
        )
        conn.executemany(
            "INSERT OR IGNORE INTO technicians (technician_name, specialization) VALUES (?, ?)",
            technicians,
        )
        conn.commit()
        print("Departments and technicians added.")
    finally:
        conn.close()


if __name__ == "__main__":
    # This block runs only when you execute: python database.py
    create_tables()
    insert_lookup_data()