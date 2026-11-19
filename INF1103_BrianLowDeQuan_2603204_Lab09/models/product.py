from abc import ABC, abstractmethod
from models.interfaces import CanBeShipped
from models.supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier):
        if price <= 0:
            raise ValueError("Product price must be greater than zero.")
        if stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = stock_quantity
        self.supplier = supplier

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

    def update_stock(self, new_stock: int) -> None:
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock = new_stock

    def display_information(self) -> None:
        print(f"ID: {self._product_id}\nName: {self._name}\nPrice: ${self._price:.2f}\nStock: {self._stock}")
        print(f"Supplier: {self.supplier.name} ({self.supplier.contact_email})")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @classmethod
    def from_dict(cls, data: dict, supplier_lookup: dict[str, Supplier]) -> "Product":
        from models.factory import ProductFactory

        product_type = data.get("type", "physical")
        sup_data = data.get("supplier")

        if sup_data and sup_data["supplier_id"] in supplier_lookup:
            supplier = supplier_lookup[sup_data["supplier_id"]]
        elif sup_data:
            supplier = Supplier.from_dict(sup_data)
            supplier_lookup[supplier.supplier_id] = supplier
        else:
            supplier = Supplier("S000", "Default Supplier", "support@supplier.com")

        return ProductFactory.create(
            product_type=product_type,
            product_id=data["id"],
            name=data["name"],
            price=float(data["price"]),
            stock_quantity=int(data["stock"]),
            supplier=supplier,
            weight=float(data.get("weight", 1.0)),
            download_size=float(data.get("download_size", 100.0)),
        )


class PhysicalProduct(Product, CanBeShipped):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        weight: float = 1.0,
    ):
        super().__init__(product_id, name, price, stock_quantity, supplier)
        if weight <= 0:
            raise ValueError("Product weight must be greater than zero.")
        self._weight = weight

    @property
    def weight(self) -> float:
        return self._weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Type: Physical Product\nWeight: {self._weight:.2f} kg")
        print(f"Fulfillment: {self.get_fulfilment_info()}")
        print(f"Estimated Shipping: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping to destination address."

    def calculate_shipping_cost(self) -> float:
        return max(3.00, self._weight * 5.00)

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "id": self._product_id,
            "name": self._name,
            "price": self._price,
            "stock": self._stock,
            "weight": self._weight,
            "supplier": self.supplier.to_dict(),
        }


class DigitalProduct(Product):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        download_size: float = 100.0,
    ):
        super().__init__(product_id, name, price, stock_quantity, supplier)
        if download_size <= 0:
            raise ValueError("Download size must be greater than zero.")
        self._download_size = download_size

    @property
    def download_size(self) -> float:
        return self._download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Type: Digital Product\nDownload Size: {self._download_size:.1f} MB")
        print(f"Fulfillment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via instant download link upon purchase."

    def to_dict(self) -> dict:
        return {
            "type": "digital",
            "id": self._product_id,
            "name": self._name,
            "price": self._price,
            "stock": self._stock,
            "download_size": self._download_size,
            "supplier": self.supplier.to_dict(),
        }
