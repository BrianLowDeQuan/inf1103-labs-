from models.supplier import Supplier
from models.product import Product, PhysicalProduct, DigitalProduct
from models.order import Order
from inventory import Inventory
from file_manager import load_inventory, save_inventory


def show_product_details(product: Product) -> None:
    """Accepts any Product subclass interchangeably without type checking."""
    product.display_information()
    print(f"Fulfilment Check: {product.get_fulfilment_info()}")


def handle_add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    prod_type_choice = input("Select product type (1 or 2): ").strip()

    if prod_type_choice not in ["1", "2"]:
        print("Invalid product type selection. Add product canceled.\n")
        return

    # Select or Create Supplier
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

    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())

        if prod_type_choice == "1":
            weight = float(input("Weight (kg): ").strip())
            new_prod: Product = PhysicalProduct(next_id, name, price, stock, supplier, weight)
        else:
            download_size = float(input("Download Size (MB): ").strip())
            new_prod = DigitalProduct(next_id, name, price, stock, supplier, download_size)

    except ValueError:
        print("Invalid input for numeric fields. Add product canceled.\n")
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
            new_stock = int(input("New Stock Quantity: ").strip())
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

        try:
            qty = int(input(f"Enter quantity for {prod.name} (Available: {prod.stock}): ").strip())
            if qty > prod.stock:
                print("Insufficient stock available.")
                continue
            order.add_order_line(prod, qty)
            prod.update_stock(prod.stock - qty)
            print(f"Added {qty} x {prod.name} to {order_id}.")
        except ValueError as e:
            print(f"Invalid quantity: {e}")

    if order.order_lines:
        orders.append(order)
        order.display_order()
    else:
        print("Empty order discarded.\n")


def run_lab8_relationship_tests() -> None:
    """Runs verification tests for Association, Aggregation, Composition, LSP, and Polymorphism."""
    print("\n================ LAB 8 RELATIONSHIP & LSP TESTS ================")

    print("\n[Test 1: Association - Supplier & Product]")
    sup = Supplier("S999", "Global Hardware Corp", "orders@globalhw.com")
    p_phys = PhysicalProduct("T001", "Mechanical Keyboard", 120.0, 10, sup, 1.2)
    p_dig = DigitalProduct("T002", "Cloud IDE Pro", 60.0, 50, sup, 450.0)
    del sup
    print("Deleted local 'sup' variable. Checking product supplier references:")
    p_phys.display_information()
    print()
    p_dig.display_information()

    print("\n[Test 2: Aggregation - Transferring Product between Inventories]")
    inv_a = Inventory("Warehouse A")
    inv_b = Inventory("Warehouse B")
    inv_a.add_product(p_phys)
    inv_a.add_product(p_dig)
    transferred = inv_a.remove_product("T001")
    if transferred:
        inv_b.add_product(transferred)
    print(f"Warehouse A count: {len(inv_a.products)} | Warehouse B count: {len(inv_b.products)}")
    print(f"Transferred product still intact: {transferred.name} (${transferred.price:.2f})")

    print("\n[Test 3: Composition - Order & OrderLine]")
    order1 = Order("ORD-TEST-1")
    order2 = Order("ORD-TEST-2")
    order1.add_order_line(p_phys, 2)
    order1.add_order_line(p_dig, 1)
    order2.add_order_line(p_phys, 3) 
    order1.display_order()
    order2.display_order()
    same_product = order1.order_lines[0].product is order2.order_lines[0].product
    different_lines = order1.order_lines[0] is not order2.order_lines[0]
    print(f"Same Product object shared? {same_product} | Distinct OrderLine objects? {different_lines}")

    print("\n[Test 4: Polymorphism & LSP via Inventory]")
    for item in inv_b.products:
        show_product_details(item)
    print("================================================================\n")


def display_menu() -> None:
    print("---------------- MENU ----------------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product from Inventory")
    print("6. Create Customer Order")
    print("7. View All Orders")
    print("8. Run Lab 8 Relationship & LSP Tests")
    print("9. Save Inventory")
    print("10. Exit")
    print("--------------------------------------")


def main() -> None:
    print("==================================================")
    print("INVENTORY & ORDER MANAGEMENT SYSTEM (LAB 8)")
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
            run_lab8_relationship_tests()
        elif choice == "9":
            print("\nSaving inventory...")
            save_inventory(inventory)
        elif choice == "10":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid choice! Please select an option from 1 to 10.\n")


if __name__ == "__main__":
    main()