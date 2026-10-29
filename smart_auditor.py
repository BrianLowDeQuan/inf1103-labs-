import json
import os

FILENAME = "inventory.json"


# --------------------------------------
# Product Class
# --------------------------------------
class Product:
    """
    Represents an individual product item in the inventory.
    Encapsulates product data and operations related to the product state.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = stock

    # Getters / Properties
    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock




def display_menu() -> None:
    """Prints the main menu options."""
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