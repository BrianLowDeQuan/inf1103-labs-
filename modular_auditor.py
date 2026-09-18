def get_valid_input():
    """
    Handles prompt, input validation, and returns a valid integer or 'quit'.
    Tracks failed entries internally until a valid entry or 'quit' is provided.
    """
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
    """Calculates the new total inventory and returns it."""
    return current_total + new_value


def calculate_tax(amount):
    """Calculates 10% tax for a specific delivery amount."""
    return amount * 0.10


def generate_report(total_units, failed_attempts, total_tax, deliveries_count):
    """Prints the final summary report."""
    print("\n--- Summary Report ---")
    print(f"Total Deliveries Processed: {deliveries_count}")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Tax Calculated (10%): {total_tax:.2f}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    total_inventory = 0
    failed_entries = 0
    total_tax = 0.0
    deliveries_processed = 0

    while True:
        result, failed_count = get_valid_input()
        failed_entries += failed_count

        if result == "quit":
            break

        # Process valid delivery
        total_inventory = process_delivery(total_inventory, result)
        tax_for_delivery = calculate_tax(result)
        total_tax += tax_for_delivery
        deliveries_processed += 1

        # Check for overstock limit
        if total_inventory >= 500:
            print("OVERSTOCK ALERT: Inventory has exceeded 500 units!")
            break

    # Generate final report
    generate_report(total_inventory, failed_entries, total_tax, deliveries_processed)


if __name__ == "__main__":
    main()