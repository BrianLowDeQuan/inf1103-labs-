from models.product import Product, PhysicalProduct

class Inventory:
    def __init__(self):
        self._products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self._products.append(product)

    def search_product(self, product_id: str) -> Product | None:
        target_id = product_id.upper()
        for prod in self._products:
            if prod.product_id.upper() == target_id:
                return prod
        return None

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("--------------------------------------------------")
        if not self._products:
            print("No items in inventory.")
        else:
            for prod in self._products:
                prod_type = "Physical" if isinstance(prod, PhysicalProduct) else "Digital"
                print(
                    f"[{prod_type}] ID: {prod.product_id} | Name: {prod.name} | "
                    f"Price: ${prod.price:.2f} | Stock: {prod.stock}"
                )
        print("--------------------------------------------------\n")

    def get_next_product_id(self) -> str:
        max_id_num = 0
        for prod in self._products:
            item_id = prod.product_id
            if item_id.startswith("P") and item_id[1:].isdigit():
                num = int(item_id[1:])
                if num > max_id_num:
                    max_id_num = num
        return f"P{max_id_num + 1:03d}"

    def to_list_of_dicts(self) -> list[dict]:
        return [prod.to_dict() for prod in self._products]

    def load_from_list_of_dicts(self, raw_data: list[dict]) -> None:
        self._products = [Product.from_dict(item) for item in raw_data]