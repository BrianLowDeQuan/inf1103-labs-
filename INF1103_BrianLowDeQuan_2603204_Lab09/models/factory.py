from models.product import Product, PhysicalProduct, DigitalProduct
from models.supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        weight: float = 1.0,
        download_size: float = 100.0,
    ) -> Product:
        normalized_type = product_type.strip().lower()
        if normalized_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, weight)
        elif normalized_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, download_size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
