import csv
import json
import os
from inventory import Inventory
from models.supplier import Supplier
from models.product import Product
from models.factory import ProductFactory

FILENAME = "inventory.json"


def load_inventory(filename: str = FILENAME) -> tuple[Inventory, dict[str, Supplier]]:
    inv = Inventory("Primary Inventory")
    suppliers: dict[str, Supplier] = {}

    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                inv.products = [Product.from_dict(item, suppliers) for item in raw_data]
                print(f"{filename} found. Inventory loaded successfully.\n")
                return inv, suppliers
        except (json.JSONDecodeError, KeyError, ValueError, OSError) as e:
            print(f"Error loading {filename}: {e}\n")

    s1 = Supplier("S001", "TechDistributors Pte Ltd", "sales@techdist.sg")
    s2 = Supplier("S002", "CyberSoft Global", "licensing@cybersoft.io")
    suppliers[s1.supplier_id] = s1
    suppliers[s2.supplier_id] = s2

    inv.add_product(ProductFactory.create("physical", "P001", "Laptop", 1200.00, 15, s1, weight=2.2))
    inv.add_product(ProductFactory.create("physical", "P002", "Mouse", 25.50, 40, s1, weight=0.15))
    inv.add_product(ProductFactory.create("digital", "P003", "Antivirus License", 45.00, 99, s2, download_size=250.0))
    return inv, suppliers


def save_inventory(inventory: Inventory, filename: str = FILENAME) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(inventory.to_list_of_dicts(), f, indent=4)
        print("Inventory saved successfully to inventory.json.\n")
    except (OSError, TypeError) as e:
        print(f"Error saving to {filename}: {e}\n")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, mode="r", encoding="utf-8", newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip header row
            for row in reader:
                if not row:
                    continue
                try:
                    if len(row) != 5:
                        raise ValueError("Expected 5 columns (product_type, product_id, name, price, stock_quantity).")
                    product_type, product_id, name, price_str, stock_str = [col.strip() for col in row]
                    price = float(price_str)
                    stock_quantity = int(stock_str)
                    product = ProductFactory.create(
                        product_type, product_id, name, price, stock_quantity, supplier
                    )
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as e:
                    print(f"Skipping invalid row {row}: {e}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
