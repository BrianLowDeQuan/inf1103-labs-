from abc import ABC, abstractmethod
from models.interfaces import CanBeShipped

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = stock

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
        print(f"ID: {self._product_id}")
        print(f"Name: {self._name}")
        print(f"Price: ${self._price:.2f}")
        print(f"Stock: {self._stock}")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @classmethod
    def from_dict(cls, data: dict):
        product_type = data.get("type", "physical")
        if product_type == "physical":
            return PhysicalProduct(
                product_id=data["id"],
                name=data["name"],
                price=float(data["price"]),
                stock=int(data["stock"]),
                weight=float(data.get("weight", 1.0)),
            )
        elif product_type == "digital":
            return DigitalProduct(
                product_id=data["id"],
                name=data["name"],
                price=float(data["price"]),
                stock=int(data["stock"]),
                download_size=float(data.get("download_size", 100.0)),
            )
        else:
            raise ValueError(f"Unknown product type: {product_type}")


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        super().__init__(product_id, name, price, stock)
        self._weight = weight

    @property
    def weight(self) -> float:
        return self._weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self._weight:.2f} kg")
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
        }


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        self._download_size = download_size

    @property
    def download_size(self) -> float:
        return self._download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self._download_size:.1f} MB")
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
        }