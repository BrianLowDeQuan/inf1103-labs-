from models.product import Product
from models.discount import DiscountStrategy, NoDiscount


class OrderLine:
    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product = product
        self.quantity = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_line(self) -> None:
        print(
            f"  - {self.product.name} (ID: {self.product.product_id}) | "
            f"Qty: {self.quantity} x ${self.product.price:.2f} = ${self.calculate_subtotal():.2f}"
        )


class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):
        self.order_id = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        self.order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> bool:
        target_id = product_id.upper()
        for i, line in enumerate(self.order_lines):
            if line.product.product_id.upper() == target_id:
                self.order_lines.pop(i)
                return True
        return False

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display_order(self) -> None:
        print(f"\nOrder ID: {self.order_id}\n--------------------------------------------------")
        if not self.order_lines:
            print("  (No items in this order)")
        else:
            for line in self.order_lines:
                line.display_line()
        raw_subtotal = sum(line.calculate_subtotal() for line in self.order_lines)
        print("--------------------------------------------------")
        print(f"Subtotal: ${raw_subtotal:.2f} | Discount Strategy: {type(self.discount).__name__}")
        print(f"Order Total: ${self.calculate_total():.2f}\n")
