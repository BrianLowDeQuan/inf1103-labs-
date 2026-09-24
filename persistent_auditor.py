import os

INVENTORY_FILE = "inventory.txt"


def load_inventory(filename=INVENTORY_FILE):
    transactions = []
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and line.isdigit():
                        transactions.append(int(line))
        except Exception as e:
            print(f"Warning: Could not load existing file ({e}). Starting fresh.")
    return transactions


def save_inventory(transactions, filename=INVENTORY_FILE):
    """
    Writes all entries from the transaction history list to inventory.txt.
    """
    try:
        with open(filename, "w") as f:
            for amount in transactions:
                f.write(f"{amount}\n")
        print(f"Inventory successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to file: {e}")


def get_valid_input():
    failed_in_prompt = 0
    while True:
        user_input = input("Enter stock quantity (or type 'quit' to exit): ").strip()

        if user_input.lower() == "quit":
            return "quit", failed_in_prompt

        if user_input.startswith("-"):
            print("Error: Negative numbers are not allowed.")
            failed_in_prompt += 1
            continue

        if not user_input.isdigit():
            print("Error: Invalid input. Please enter a valid non-negative integer.")
            failed_in_prompt += 1
            continue

        return int(user_input), failed_in_prompt


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts, total_tax, deliveries_count, history):
    print("\n--- Summary Report ---")
    print(f"Transaction History (List): {history}")
    print(f"Total Deliveries Processed: {deliveries_count}")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Tax Calculated (10%): {total_tax:.2f}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    history = load_inventory()
    
    total_inventory = sum(history)
    failed_entries = 0
    total_tax = sum(calculate_tax(x) for x in history)
    deliveries_processed = len(history)

    while True:
        result, failed_count = get_valid_input()
        failed_entries += failed_count

        if result == "quit":
            break

        history.append(result)

        total_inventory = process_delivery(total_inventory, result)
        tax_for_delivery = calculate_tax(result)
        total_tax += tax_for_delivery
        deliveries_processed += 1

        if total_inventory >= 500:
            print("OVERSTOCK ALERT: Inventory has reached/exceeded 500 units!")
            break

    # Save data before exiting
    save_inventory(history)
    generate_report(total_inventory, failed_entries, total_tax, deliveries_processed, history)


if __name__ == "__main__":
    main()