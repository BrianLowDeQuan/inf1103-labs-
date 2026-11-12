from models.product import Product

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Order line quantity must be greater than zero.")
        self.product = product
        self.quantity = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_line(self) -> None:
        print(f"  - {self.product.name} (ID: {self.product.product_id}) | Qty: {self.quantity} x ${self.product.price:.2f} = ${self.calculate_subtotal():.2f}")


class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        self.order_lines.append(OrderLine(product, quantity))

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order(self) -> None:
        print(f"\nOrder ID: {self.order_id}\n--------------------------------------------------")
        if not self.order_lines:
            print("  (No items in this order)")
        else:
            for line in self.order_lines:
                line.display_line()
        print(f"--------------------------------------------------\nOrder Total: ${self.calculate_total():.2f}\n")