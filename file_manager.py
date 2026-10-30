import json
import os
from inventory import Inventory

FILENAME = "inventory.json"

def load_inventory(filename=FILENAME) -> Inventory:
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

    default_items = [
        {"type": "physical", "id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15, "weight": 2.2},
        {"type": "physical", "id": "P002", "name": "Mouse", "price": 25.50, "stock": 40, "weight": 0.15},
        {"type": "digital", "id": "P003", "name": "Antivirus License", "price": 45.00, "stock": 99, "download_size": 250.0},
    ]
    inv.load_from_list_of_dicts(default_items)
    return inv

def save_inventory(inventory: Inventory, filename=FILENAME) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(inventory.to_list_of_dicts(), f, indent=4)
        print("Inventory saved successfully to inventory.json.\n")
    except Exception as e:
        print(f"Error saving to {filename}: {e}\n")