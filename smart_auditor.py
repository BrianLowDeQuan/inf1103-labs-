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

    # Encapsulated state management
    def update_stock(self, new_stock: int) -> None:
        """Updates the stock quantity internally."""
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock = new_stock

    def display_information(self) -> None:
        """Displays formatted product details."""
        print(f"ID: {self._product_id}")
        print(f"Name: {self._name}")
        print(f"Price: ${self._price:.2f}")
        print(f"Stock: {self._stock}")

    def to_dict(self) -> dict:
        """Converts Product object back to dictionary for JSON serialization."""
        return {
            "id": self._product_id,
            "name": self._name,
            "price": self._price,
            "stock": self._stock,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Factory method to instantiate a Product from a dictionary."""
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=float(data["price"]),
            stock=int(data["stock"]),
        )


# --------------------------------------
# Inventory Class
# --------------------------------------
class Inventory:
    """
    Manages a collection of Product objects.
    Provides operational methods to add, search, and display products.
    """

    def __init__(self):
        self._products: list[Product] = []

    def add_product(self, product: Product) -> None:
        """Adds a Product instance to the collection."""
        self._products.append(product)

    def search_product(self, product_id: str) -> Product | None:
        """Searches for a product by its ID (case-insensitive)."""
        target_id = product_id.upper()
        for prod in self._products:
            if prod.product_id.upper() == target_id:
                return prod
        return None

    def display_all(self) -> None:
        """Displays all products in the inventory."""
        print("\nCurrent Inventory")
        print("--------------------------------------------------")
        if not self._products:
            print("No items in inventory.")
        else:
            for prod in self._products:
                print(
                    f"ID: {prod.product_id} | Name: {prod.name} | "
                    f"Price: ${prod.price:.2f} | Stock: {prod.stock}"
                )
        print("--------------------------------------------------\n")

    def get_next_product_id(self) -> str:
        """Generates the next auto-incrementing Product ID (e.g., P004)."""
        max_id_num = 0
        for prod in self._products:
            item_id = prod.product_id
            if item_id.startswith("P") and item_id[1:].isdigit():
                num = int(item_id[1:])
                if num > max_id_num:
                    max_id_num = num
        return f"P{max_id_num + 1:03d}"

    def to_list_of_dicts(self) -> list[dict]:
        """Converts all products to dictionaries for JSON export."""
        return [prod.to_dict() for prod in self._products]

    def load_from_list_of_dicts(self, raw_data: list[dict]) -> None:
        """Populates inventory from loaded raw dictionary data."""
        self._products = [Product.from_dict(item) for item in raw_data]


# --------------------------------------
# File Handling Functions
# --------------------------------------
def load_inventory(filename=FILENAME) -> Inventory:
    """Loads inventory data from inventory.json into an Inventory instance."""
    inv = Inventory()
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                inv.load_from_list_of_dicts(raw_data)
                print(f"{filename} found.")
                print("Inventory loaded successfully.\n")
                return inv
        except Exception as e:
            print(f"Error loading {filename}: {e}\n")

    # Initial default products if inventory.json is missing/unusable
    default_items = [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
    ]
    inv.load_from_list_of_dicts(default_items)
    return inv


def save_inventory(inventory: Inventory, filename=FILENAME) -> None:
    """Saves the inventory collection to inventory.json."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(inventory.to_list_of_dicts(), f, indent=4)
        print("Inventory saved successfully to inventory.json.\n")
    except Exception as e:
        print(f"Error saving to {filename}: {e}\n")


# --------------------------------------
# User Interface & Interaction Logic
# --------------------------------------
def handle_add_product(inventory: Inventory) -> None:
    """Handles CLI user interaction for adding a product."""
    print("\nAdd New Product")
    next_id = inventory.get_next_product_id()
    print(f"Product ID: {next_id}")

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("Invalid input for price or stock quantity. Add product canceled.\n")
        return

    new_prod = Product(next_id, name, price, stock)
    inventory.add_product(new_prod)
    print("\nProduct added successfully!\n")


def handle_update_stock(inventory: Inventory) -> None:
    """Handles CLI user interaction for updating stock."""
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
    """Handles CLI user interaction for searching a product."""
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