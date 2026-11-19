from models.supplier import Supplier
from models.product import Product
from models.factory import ProductFactory
from models.order import Order
from models.discount import (
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount,
)
from inventory import Inventory
from file_manager import load_inventory, save_inventory, load_products


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter zero or a positive whole number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 10")


def get_positive_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a whole number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 1")


def show_product_details(product: Product) -> None:
    """Accepts any Product subclass interchangeably without type checking."""
    product.display_information()
    print(f"Fulfilment Check: {product.get_fulfilment_info()}")


def handle_add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    prod_type_choice = input("Select product type (1 or 2): ").strip()

    if prod_type_choice == "1":
        product_type = "physical"
    elif prod_type_choice == "2":
        product_type = "digital"
    else:
        print("Invalid product type selection. Add product canceled.\n")
        return

    print("\nAvailable Suppliers:")
    for sup in suppliers.values():
        sup.display_information()
    sup_id = input("Enter Supplier ID (or type NEW to register a new supplier): ").strip().upper()

    if sup_id == "NEW" or sup_id not in suppliers:
        if sup_id != "NEW":
            print(f"Supplier '{sup_id}' not found. Registering new supplier...")
        new_sup_id = input("New Supplier ID (e.g., S003): ").strip().upper()
        sup_name = input("Supplier Name: ").strip()
        sup_email = input("Supplier Contact Email: ").strip()
        supplier = Supplier(new_sup_id, sup_name, sup_email)
        suppliers[new_sup_id] = supplier
    else:
        supplier = suppliers[sup_id]

    next_id = inventory.get_next_product_id()
    print(f"\nAssigned Product ID: {next_id}")
    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty. Add product canceled.\n")
        return

    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")

    try:
        if product_type == "physical":
            weight = get_positive_float("Weight (kg): ")
            new_prod = ProductFactory.create(
                product_type, next_id, name, price, stock, supplier, weight=weight
            )
        else:
            download_size = get_positive_float("Download Size (MB): ")
            new_prod = ProductFactory.create(
                product_type, next_id, name, price, stock, supplier, download_size=download_size
            )
    except ValueError as e:
        print(f"Unable to create product: {e}\n")
        return

    inventory.add_product(new_prod)
    print("\nProduct added successfully!\n")


def handle_update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    prod_id = input("Enter Product ID: ").strip()

    prod = inventory.find_product(prod_id)
    if prod:
        print(f"\nProduct Found: {prod.name} (Current Stock: {prod.stock})")
        try:
            new_stock = get_non_negative_int("New Stock Quantity: ")
            prod.update_stock(new_stock)
            print("\nStock updated successfully!\n")
        except ValueError as e:
            print(f"Invalid input: {e}\n")
    else:
        print("Product not found.\n")


def handle_search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    prod_id = input("Enter Product ID: ").strip()

    prod = inventory.find_product(prod_id)
    if prod:
        print("\nProduct Found")
        print("--------------------------------------------------")
        show_product_details(prod)
        print("--------------------------------------------------\n")
    else:
        print("Product not found.\n")


def handle_remove_product(inventory: Inventory) -> None:
    print("\nRemove Product from Inventory")
    prod_id = input("Enter Product ID to remove: ").strip()

    removed = inventory.remove_product(prod_id)
    if removed:
        print(f"\nRemoved '{removed.name}' ({removed.product_id}) from {inventory.name}.")
        print("Note: The Product object still exists independently in memory.\n")
    else:
        print("Product not found.\n")


def choose_discount_strategy() -> DiscountStrategy:
    print("\nSelect Order Discount Strategy:")
    print("1. No Discount (0%)")
    print("2. Percentage Discount (10% off)")
    print("3. Bulk Discount ($20 off orders >= $200)")
    print("4. Student Discount (5% off)")
    choice = input("Choose discount option (1-4, default 1): ").strip()

    if choice == "2":
        return PercentageDiscount(10)
    elif choice == "3":
        return BulkDiscount(200, 20)
    elif choice == "4":
        return StudentDiscount(5)
    return NoDiscount()


def handle_create_order(inventory: Inventory, orders: list[Order]) -> None:
    order_id = f"ORD{len(orders) + 1:03d}"
    order = Order(order_id)
    print(f"\nCreating New Order ({order_id})")

    while True:
        prod_id = input("Enter Product ID to add to order (or DONE to finish): ").strip()
        if prod_id.upper() == "DONE":
            break

        prod = inventory.find_product(prod_id)
        if not prod:
            print("Product not found in inventory.")
            continue

        qty = get_positive_int(f"Enter quantity for {prod.name} (Available: {prod.stock}): ")
        if qty > prod.stock:
            print("Insufficient stock available.")
            continue

        try:
            order.add_order_line(prod, qty)
            prod.update_stock(prod.stock - qty)
            print(f"Added {qty} x {prod.name} to {order_id}.")
        except ValueError as e:
            print(f"Invalid quantity: {e}")

    if order.order_lines:
        order.set_discount(choose_discount_strategy())
        orders.append(order)
        order.display_order()
    else:
        print("Empty order discarded.\n")


def handle_load_products_csv(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nBulk Load Products from CSV")
    path = input("Enter CSV file path (default: products.csv): ").strip() or "products.csv"
    default_supplier = next(
        iter(suppliers.values()),
        Supplier("S000", "Default Supplier", "support@supplier.com"),
    )
    load_products(path, inventory, default_supplier)
    print()


def run_lab9_verification_tests() -> None:
    """Runs verification checks for Strategy, Factory, Validation, and CSV Exception Handling."""
    print("\n================ LAB 9 DESIGN PATTERNS & ERROR HANDLING TESTS ================")

    sup = Supplier("S999", "Global Hardware Corp", "orders@globalhw.com")
    p_phys = ProductFactory.create("physical", "T001", "Mechanical Keyboard", 125.0, 10, sup, weight=1.2)
    p_dig = ProductFactory.create("digital", "T002", "Cloud IDE Pro", 60.0, 50, sup, download_size=450.0)

    print("\n[Test 1: Strategy Pattern - Interchangeable Order Discounts]")
    order = Order("ORD-STRAT-1")
    order.add_order_line(p_phys, 2)  # 2 * 125.0 = 250.0
    print(f"Subtotal ($250.00) with NoDiscount: ${order.calculate_total():.2f}")
    order.set_discount(BulkDiscount(200, 20))
    print(f"Subtotal ($250.00) with BulkDiscount(200, 20): ${order.calculate_total():.2f}")
    order.set_discount(PercentageDiscount(10))
    print(f"Subtotal ($250.00) with PercentageDiscount(10): ${order.calculate_total():.2f}")
    order.set_discount(StudentDiscount())
    print(f"Subtotal ($250.00) with StudentDiscount(5%): ${order.calculate_total():.2f}")

    print("\n[Test 2: Factory Pattern - Unknown Type Handling]")
    try:
        ProductFactory.create("service", "S001", "Installation", 30.0, 5, sup)
    except ValueError as e:
        print(f"Caught expected ValueError from ProductFactory: {e}")

    print("\n[Test 3: Validation Rules]")
    for label, fn in [
        ("Negative price", lambda: ProductFactory.create("physical", "X1", "Bad", -10.0, 5, sup)),
        ("Negative stock", lambda: ProductFactory.create("digital", "X2", "Bad", 10.0, -1, sup)),
        ("Zero order quantity", lambda: order.add_order_line(p_dig, 0)),
    ]:
        try:
            fn()
        except ValueError as e:
            print(f"{label} rejected -> {e}")

    print("\n[Test 4: CSV Loading with Exception Handling]")
    temp_inv = Inventory("CSV Test Warehouse")
    load_products("products.csv", temp_inv, sup)
    print("==============================================================================\n")


def display_menu() -> None:
    print("---------------- MENU ----------------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product from Inventory")
    print("6. Create Customer Order")
    print("7. View All Orders")
    print("8. Bulk Load Products from CSV")
    print("9. Run Lab 9 Verification Tests")
    print("10. Save Inventory")
    print("11. Exit")
    print("--------------------------------------")


def main() -> None:
    print("==================================================")
    print("INVENTORY & ORDER MANAGEMENT SYSTEM (LAB 9)")
    print("==================================================\n")

    inventory, suppliers = load_inventory()
    orders: list[Order] = []

    while True:
        display_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all_products()
        elif choice == "2":
            handle_add_product(inventory, suppliers)
        elif choice == "3":
            handle_update_stock(inventory)
        elif choice == "4":
            handle_search_product(inventory)
        elif choice == "5":
            handle_remove_product(inventory)
        elif choice == "6":
            handle_create_order(inventory, orders)
        elif choice == "7":
            if not orders:
                print("\nNo customer orders placed yet.\n")
            else:
                for order in orders:
                    order.display_order()
        elif choice == "8":
            handle_load_products_csv(inventory, suppliers)
        elif choice == "9":
            run_lab9_verification_tests()
        elif choice == "10":
            print("\nSaving inventory...")
            save_inventory(inventory)
        elif choice == "11":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid choice! Please select an option from 1 to 11.\n")


if __name__ == "__main__":
    main()
