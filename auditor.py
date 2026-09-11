total_inventory = 0
failed_entries = 0

while True:
    user_input = input("Enter stock quantity (or type 'quit' to exit): ").strip()

    # Handle user exit command
    if user_input.lower() == "quit":
        break

    # Reject negative numbers explicitly
    if user_input.startswith("-"):
        print("Error: Negative numbers are not allowed.")
        failed_entries += 1
        continue

    # Validate non-digit string inputs
    if not user_input.isdigit():
        print("Error: Invalid input. Please enter a valid non-negative integer.")
        failed_entries += 1
        continue

    # Process valid input
    quantity = int(user_input)
    total_inventory += quantity

    # Check for overstock limit
    if total_inventory > 500:
        print("OVERSTOCK ALERT: Inventory has exceeded 500 units!")
        break

# Summary report
print("\n--- Summary Report ---")
print(f"Total Units Processed: {total_inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")