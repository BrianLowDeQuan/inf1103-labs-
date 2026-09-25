# Persistent Auditor for Inventory Management base on week 2 ~ 3
# import os

# INVENTORY_FILE = "inventory.txt"


# def load_inventory(filename=INVENTORY_FILE):
#     """
#     Reads previously saved transaction history from file at startup.
#     If the file does not exist, starts with an empty history.
#     """
#     transactions = []
#     if os.path.exists(filename):
#         try:
#             with open(filename, "r") as f:
#                 for line in f:
#                     line = line.strip()
#                     if line and line.isdigit():
#                         transactions.append(int(line))
#         except Exception as e:
#             print(f"Warning: Could not load existing file ({e}). Starting fresh.")
#     return transactions


# def save_inventory(transactions, filename=INVENTORY_FILE):
#     """
#     Writes the transaction history list and total to inventory.txt upon exit.
#     """
#     try:
#         with open(filename, "w") as f:
#             for amount in transactions:
#                 f.write(f"{amount}\n")
#         print(f"\nData successfully saved to {filename}")
#     except Exception as e:
#         print(f"Error saving data to file: {e}")


# def get_valid_input():
#     """
#     Handles prompt, input validation, and returns a valid integer or 'quit'.
#     Tracks failed entries internally until a valid entry or 'quit' is provided.
#     """
#     failed_in_prompt = 0
#     while True:
#         user_input = input("Enter stock quantity (or type 'quit' to exit): ").strip()

#         if user_input.lower() == "quit":
#             return "quit", failed_in_prompt

#         if user_input.startswith("-"):
#             print("Error: Negative numbers are not allowed.")
#             failed_in_prompt += 1
#             continue

#         if not user_input.isdigit():
#             print("Error: Invalid input. Please enter a valid non-negative integer.")
#             failed_in_prompt += 1
#             continue

#         return int(user_input), failed_in_prompt


# def process_delivery(current_total, new_value):
#     """Calculates the new total inventory and returns it."""
#     return current_total + new_value


# def calculate_tax(amount):
#     """Calculates 10% tax for a specific delivery amount."""
#     return amount * 0.10


# def generate_report(total_units, failed_attempts, total_tax, deliveries_count, history):
#     """Prints the final summary report including transaction history."""
#     print("\n--- Summary Report ---")
#     print(f"Transaction History: {history}")
#     print(f"Total Deliveries Processed: {deliveries_count}")
#     print(f"Total Units Processed: {total_units}")
#     print(f"Total Tax Calculated (10%): {total_tax:.2f}")
#     print(f"Number of Failed/Rejected Entries: {failed_attempts}")


# def main():
#     # 1. Load initial data from persistence layer
#     history = load_inventory()
    
#     total_inventory = sum(history)
#     failed_entries = 0
#     total_tax = sum(calculate_tax(val) for val in history)
#     deliveries_processed = len(history)

#     if history:
#         print(f"Loaded existing history from {INVENTORY_FILE}. Initial stock: {total_inventory} units.")

#     while True:
#         result, failed_count = get_valid_input()
#         failed_entries += failed_count

#         if result == "quit":
#             break

#         # 2. Track history in memory
#         history.append(result)

#         # Process valid delivery
#         total_inventory = process_delivery(total_inventory, result)
#         tax_for_delivery = calculate_tax(result)
#         total_tax += tax_for_delivery
#         deliveries_processed += 1

#         # Check for overstock limit
#         if total_inventory >= 500:
#             print("OVERSTOCK ALERT: Inventory has reached/exceeded 500 units!")
#             break

#     # 3. Save state to file on completion
#     save_inventory(history)

#     # 4. Display final report
#     generate_report(total_inventory, failed_entries, total_tax, deliveries_processed, history)


# if __name__ == "__main__":
#     main()

#Scenario base on sample expected output
import os

FILENAME = "orders.txt"


def load_inventory(filename=FILENAME):
    """
    Reads order records from the text file into memory as a list of tuples.
    Format per line: order_id, product_name, quantity
    """
    orders = []
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(",")
                        if len(parts) == 3:
                            orders.append((parts[0].strip(), parts[1].strip(), int(parts[2].strip())))
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    return orders


def save_inventory(orders, filename=FILENAME):
    """
    Writes the updated list of orders back to the text file.
    """
    try:
        with open(filename, "w") as f:
            for order_id, name, qty in orders:
                f.write(f"{order_id},{name},{qty}\n")
        print(f"Order successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to {filename}: {e}")


def get_next_order_id(orders):
    """Generates auto-incrementing 4-digit order IDs starting from 1001."""
    if not orders:
        return 1001
    return int(orders[-1][0]) + 1


def display_current_orders(orders):
    """Displays formatted list of current orders stored in the system."""
    print("Current Orders:\n")
    if orders:
        for order_id, name, qty in orders:
            print(f"{order_id}, {name}, {qty}")
    else:
        print("No existing orders found.")
    print()


def main():
    # 1. Load existing state at startup
    orders = load_inventory()

    # 2. Display existing orders
    display_current_orders(orders)

    # 3. Prompt user for product information
    product_name = input("Enter Product Name: ").strip()
    if not product_name:
        print("Product name cannot be empty.")
        return

    try:
        quantity = int(input("Enter Quantity: ").strip())
    except ValueError:
        print("Error: Quantity must be a valid number.")
        return

    # 4. Generate Order ID and append to transaction history list
    next_id = str(get_next_order_id(orders))
    orders.append((next_id, product_name, quantity))

    # 5. Output confirmation matching sample format
    print("\nNew Order Added:")
    print(f"{next_id},{product_name},{quantity}\n")

    # 6. Save updated data back to persistence file
    save_inventory(orders)


if __name__ == "__main__":
    main()