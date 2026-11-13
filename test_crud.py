from crud import *

print("1. Create a ticket")
new_id = create_ticket("Test User", 1, "Software", "Teams app not opening", "Medium")
print("   New ticket ID:", new_id)

print("\n2. Read it back")
print("  ", get_ticket(new_id))

print("\n3. Assign technician 2 (Neha) -> should become In Progress")
assign_technician(new_id, 2)
print("  ", get_ticket(new_id))

print("\n4. Resolve it -> resolved_date should be filled")
update_status(new_id, "Resolved")
print("  ", get_ticket(new_id))

print("\n5. Search: Critical + Open tickets")
for t in search_tickets(status="Open", priority="Critical"):
    print("  ", t)

print("\n6. Search keyword 'wifi'")
for t in search_tickets(keyword="Wi-Fi"):
    print("  ", t[0], t[1], t[4])

print("\n7. Validation test (should print an error message, not crash)")
try:
    create_ticket("", 1, "Printer", "x", "Urgent")
except ValueError as e:
    print("   Caught error:", e)

print("\n8. Delete the test ticket")
print("   Deleted:", delete_ticket(new_id))
print("   Deleted again:", delete_ticket(new_id))