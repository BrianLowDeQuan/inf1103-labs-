import json
import os

FILENAME = "inventory.json"

#--------------------------------------
# Inventory load functions
#--------------------------------------
def load_inventory(filename=FILENAME):
    """
    Check whether inventory.json exists. Load inventory.json if it exists.
    Otherwise, begin with an initial list of default products if missing.
    """
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                inventory = json.load(f)
                print(f"{filename} found.")
                print("Inventory loaded successfully.\n")
                return inventory
        except Exception as e:
            print(f"Error loading {filename}: {e}\n")

    # Initial default products if inventory.json is not found
    inventory = [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
    ]
    return inventory



#--------------------------------------
# Display Inventory Functions
#--------------------------------------
def display_all(inventory):
    """Displays formatted list of current products."""
    print("\nCurrent Inventory")
    print("--------------------------------------------------")
    if not inventory:
        print("No items in inventory.")
    else:
        for item in inventory:
            print(
                f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}"
            )
    print("--------------------------------------------------\n")

#--------------------------------------
# Save Inventory Function
#--------------------------------------
def save_inventory(inventory, filename=FILENAME):
    """Saves inventory list back to inventory.json."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(inventory, f, indent=4)
        print("Inventory saved successfully to inventory.json.\n")
    except Exception as e:
        print(f"Error saving to {filename}: {e}\n")

#-------------------------------------
# Auto-generate Product ID Function
#-------------------------------------
def get_next_product_id(inventory):
    """Generates next auto-incrementing Product ID (e.g., P004)."""
    max_id_num = 0
    for item in inventory:
        item_id = item.get("id", "")
        if item_id.startswith("P") and item_id[1:].isdigit():
            num = int(item_id[1:])
            if num > max_id_num:
                max_id_num = num
    return f"P{max_id_num + 1:03d}"

#--------------------------------------
# Add Product Functions
#--------------------------------------
def add_product(inventory):
    """Prompts user to add a new product item."""
    print("\nAdd New Product")
    next_id = get_next_product_id(inventory)
    print(f"Product ID: {next_id}")

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("Invalid input for price or stock quantity. Add product canceled.\n")
        return

    new_product = {"id": next_id, "name": name, "price": price, "stock": stock}

    inventory.append(new_product)
    print("\nProduct added successfully!\n")

#--------------------------------------
# Update Stock Functions
#--------------------------------------
def update_stock(inventory):
    """Prompts user for product ID and updates its stock quantity."""
    print("\nUpdate Stock")
    prod_id = input("Enter Product ID: ").strip().upper()

    for item in inventory:
        if item["id"].upper() == prod_id:
            print("\nProduct Found:")
            print(f"Name: {item['name']}")
            print(f"Current Stock: {item['stock']}\n")
            try:
                new_stock = int(input("New Stock Quantity: ").strip())
                item["stock"] = new_stock
                print("\nStock updated successfully!\n")
            except ValueError:
                print("Invalid stock number entered.\n")
            return

    print("Product not found.\n")

#--------------------------------------
# Search Product Function
#--------------------------------------
def search_product(inventory):
    """Searches for a product by product ID and displays details."""
    print("\nSearch Product")
    prod_id = input("Enter Product ID: ").strip().upper()

    for item in inventory:
        if item["id"].upper() == prod_id:
            print("\nProduct Found")
            print("--------------------------------------------------")
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock: {item['stock']}")
            print("--------------------------------------------------\n")
            return

    print("Product not found.\n")

#--------------------------------------
# Display Menu Function
#--------------------------------------
def display_menu():
    """Prints the main interactive menu."""
    print("---------------- MENU ----------------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("--------------------------------------")


def main():
    print("==================================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("==================================================\n")

    # Load inventory at start
    inventory = load_inventory()

    while True:
        display_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid choice! Please select an option from 1 to 6.\n")


if __name__ == "__main__":
    main()