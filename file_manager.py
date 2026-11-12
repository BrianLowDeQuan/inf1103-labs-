import json
import os
from inventory import Inventory
from models.supplier import Supplier
from models.product import Product, PhysicalProduct, DigitalProduct

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
        except Exception as e:
            print(f"Error loading {filename}: {e}\n")

    s1 = Supplier("S001", "TechDistributors Pte Ltd", "sales@techdist.sg")
    s2 = Supplier("S002", "CyberSoft Global", "licensing@cybersoft.io")
    suppliers[s1.supplier_id] = s1
    suppliers[s2.supplier_id] = s2

    inv.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, s1, 2.2))
    inv.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, s1, 0.15))
    inv.add_product(DigitalProduct("P003", "Antivirus License", 45.00, 99, s2, 250.0))
    return inv, suppliers

def save_inventory(inventory: Inventory, filename: str = FILENAME) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(inventory.to_list_of_dicts(), f, indent=4)
        print("Inventory saved successfully to inventory.json.\n")
    except Exception as e:
        print(f"Error saving to {filename}: {e}\n")