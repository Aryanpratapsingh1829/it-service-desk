-- sql_examples.sql : SQL queries used in the IT Service Desk project

-- 1. CREATE (full schema is in database.py)
CREATE TABLE IF NOT EXISTS departments (
    department_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL UNIQUE
);

-- 2. INSERT: add a new ticket (status becomes 'Open' by DEFAULT)
INSERT INTO tickets (employee_name, department_id, issue_category,
                     issue_description, priority, created_date)
VALUES ('Test User', 1, 'Software', 'Teams app not opening', 'Medium', '2026-11-13 10:00:00');

-- 3. SELECT: all columns / specific columns
SELECT * FROM tickets;
SELECT employee_name, priority FROM tickets;

-- 4. WHERE: filter rows
SELECT ticket_id, employee_name, issue_description
FROM tickets
WHERE priority = 'Critical';

-- 5. WHERE with AND
SELECT * FROM tickets WHERE priority = 'High' AND status = 'Resolved';

-- 6. ORDER BY: newest first
SELECT ticket_id, employee_name, created_date
FROM tickets
ORDER BY created_date DESC;

-- 7. COUNT: total tickets
SELECT COUNT(*) AS total_tickets FROM tickets;

-- 8. GROUP BY + COUNT: tickets per status
SELECT status, COUNT(*) AS total
FROM tickets
GROUP BY status;

-- 9. GROUP BY + ORDER BY: most common category first
SELECT issue_category, COUNT(*) AS total
FROM tickets
GROUP BY issue_category
ORDER BY total DESC;

-- 10. JOIN: department name instead of department_id
SELECT t.ticket_id, t.employee_name, d.department_name, t.priority
FROM tickets t
JOIN departments d ON t.department_id = d.department_id;

-- 11. JOIN + GROUP BY: tickets per department
SELECT d.department_name, COUNT(*) AS total
FROM tickets t
JOIN departments d ON t.department_id = d.department_id
GROUP BY d.department_name
ORDER BY total DESC;

-- 12. LEFT JOIN: include tickets with NO technician (Open tickets)
SELECT t.ticket_id, t.status, tech.technician_name
FROM tickets t
LEFT JOIN technicians tech ON t.technician_id = tech.technician_id;

-- 13. UPDATE: assign technician and change status
UPDATE tickets
SET technician_id = 2, status = 'In Progress'
WHERE ticket_id = 33;

-- 14. DELETE: remove one ticket (ALWAYS use WHERE!)
DELETE FROM tickets WHERE ticket_id = 33;