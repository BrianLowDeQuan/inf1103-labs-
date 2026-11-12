from models.product import Product

class Inventory:
    def __init__(self, name: str = "Main Warehouse"):
        self.name = name
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        target_id = product_id.upper()
        for i, product in enumerate(self.products):
            if product.product_id.upper() == target_id:
                return self.products.pop(i)
        return None

    def find_product(self, product_id: str) -> Product | None:
        target_id = product_id.upper()
        for product in self.products:
            if product.product_id.upper() == target_id:
                return product
        return None

    def display_all_products(self) -> None:
        print(f"\nCurrent Inventory ({self.name})\n==================================================")
        if not self.products:
            print("No items in inventory.")
        else:
            for product in self.products:
                product.display_information()
                print("--------------------------------------------------")
        print()

    def get_next_product_id(self) -> str:
        max_id_num = 0
        for prod in self.products:
            item_id = prod.product_id
            if item_id.startswith("P") and item_id[1:].isdigit():
                num = int(item_id[1:])
                if num > max_id_num:
                    max_id_num = num
        return f"P{max_id_num + 1:03d}"

    def to_list_of_dicts(self) -> list[dict]:
        return [prod.to_dict() for prod in self.products]