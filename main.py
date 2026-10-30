from inventory import Inventory
from models.product import PhysicalProduct, DigitalProduct
from file_manager import load_inventory, save_inventory

def handle_add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    prod_type_choice = input("Select product type (1 or 2): ").strip()

    if prod_type_choice not in ["1", "2"]:
        print("Invalid product type selection. Add product canceled.\n")
        return

    next_id = inventory.get_next_product_id()
    print(f"Product ID: {next_id}")

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())

        if prod_type_choice == "1":
            weight = float(input("Weight (kg): ").strip())
            new_prod = PhysicalProduct(next_id, name, price, stock, weight)
        else:
            download_size = float(input("Download Size (MB): ").strip())
            new_prod = DigitalProduct(next_id, name, price, stock, download_size)

    except ValueError:
        print("Invalid input for numeric fields. Add product canceled.\n")
        return

    inventory.add_product(new_prod)
    print("\nProduct added successfully!\n")

def handle_update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    prod_id = input("Enter Product ID: ").strip()

    prod = inventory.search_product(prod_id)
    if prod:
        print("\nProduct Found:")
        print(f"Name: {prod.name}")
        print(f"Current Stock: {prod.stock}\n")
        try:
            new_stock = int(input("New Stock Quantity: ").strip())
            prod.update_stock(new_stock)
            print("\nStock updated successfully!\n")
        except ValueError as e:
            print(f"Invalid input: {e}\n")
    else:
        print("Product not found.\n")

def handle_search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    prod_id = input("Enter Product ID: ").strip()

    prod = inventory.search_product(prod_id)
    if prod:
        print("\nProduct Found")
        print("--------------------------------------------------")
        prod.display_information()
        print("--------------------------------------------------\n")
    else:
        print("Product not found.\n")

def display_menu() -> None:
    print("---------------- MENU ----------------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("--------------------------------------")

def main() -> None:
    print("==================================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("==================================================\n")

    inventory = load_inventory()

    while True:
        display_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            handle_add_product(inventory)
        elif choice == "3":
            handle_update_stock(inventory)
        elif choice == "4":
            handle_search_product(inventory)
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