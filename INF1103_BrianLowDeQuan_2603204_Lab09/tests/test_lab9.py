import os
import tempfile
import unittest
from unittest.mock import patch

from inventory import Inventory
from file_manager import load_products
from main import get_positive_float
from models.discount import (
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount,
)
from models.factory import ProductFactory
from models.order import Order, OrderLine
from models.product import Product, PhysicalProduct, DigitalProduct
from models.supplier import Supplier


class TestDiscountStrategies(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechDistributors", "sales@techdist.sg")
        self.item = ProductFactory.create("physical", "P001", "Monitor", 250.0, 10, self.supplier)

    def test_default_order_uses_no_discount(self):
        order = Order("ORD001")
        order.add_order_line(self.item, 1)
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertAlmostEqual(order.calculate_total(), 250.0)

    def test_bulk_discount_above_and_below_threshold(self):
        order = Order("ORD002", BulkDiscount(200, 20))
        order.add_order_line(self.item, 1)  # 250 >= 200
        self.assertAlmostEqual(order.calculate_total(), 230.0)

        cheap_item = ProductFactory.create("digital", "D001", "E-Book", 50.0, 20, self.supplier)
        small_order = Order("ORD003", BulkDiscount(200, 20))
        small_order.add_order_line(cheap_item, 2)  # 100 < 200
        self.assertAlmostEqual(small_order.calculate_total(), 100.0)

    def test_set_discount_swaps_strategy_at_runtime(self):
        order = Order("ORD004", BulkDiscount(200, 20))
        order.add_order_line(self.item, 1)
        self.assertAlmostEqual(order.calculate_total(), 230.0)

        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_fourth_strategy_student_discount_without_changing_order(self):
        order = Order("ORD005", StudentDiscount())  # 5% student discount
        order.add_order_line(self.item, 1)
        self.assertAlmostEqual(order.calculate_total(), 237.5)

    def test_shared_discount_strategy_across_orders(self):
        shared_promo = PercentageDiscount(10)
        order_a = Order("ORD-A", shared_promo)
        order_b = Order("ORD-B", shared_promo)
        order_a.add_order_line(self.item, 1)
        order_b.add_order_line(self.item, 2)
        self.assertIs(order_a.discount, order_b.discount)
        self.assertAlmostEqual(order_a.calculate_total(), 225.0)
        self.assertAlmostEqual(order_b.calculate_total(), 450.0)


class TestProductFactory(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechDistributors", "sales@techdist.sg")

    def test_create_physical_and_digital_products(self):
        phys = ProductFactory.create("physical", "P001", "Laptop", 1200.0, 5, self.supplier)
        dig = ProductFactory.create("digital", "D001", "License", 49.9, 50, self.supplier)
        self.assertIsInstance(phys, PhysicalProduct)
        self.assertIsInstance(phys, Product)
        self.assertIsInstance(dig, DigitalProduct)
        self.assertIsInstance(dig, Product)

    def test_unknown_product_type_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "S001", "Installation", 30.0, 5, self.supplier)
        self.assertIn("Unknown product type", str(ctx.exception))


class TestValidationRules(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechDistributors", "sales@techdist.sg")
        self.valid_product = ProductFactory.create("physical", "P001", "Mouse", 25.0, 10, self.supplier)

    def test_product_price_must_be_greater_than_zero(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P002", "Zero Price", 0.0, 5, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D002", "Negative Price", -15.0, 5, self.supplier)

    def test_product_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P003", "Neg Stock", 10.0, -1, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D003", "Neg Digital Stock", 10.0, -5, self.supplier)
        with self.assertRaises(ValueError):
            self.valid_product.update_stock(-2)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        with self.assertRaises(ValueError):
            OrderLine(self.valid_product, 0)
        with self.assertRaises(ValueError):
            OrderLine(self.valid_product, -3)


class TestExceptionHandlingAndCSV(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechDistributors", "sales@techdist.sg")

    @patch("builtins.input", side_effect=["abc", "-5", "12.50"])
    @patch("builtins.print")
    def test_get_positive_float_reprompts_until_valid(self, mock_print, mock_input):
        result = get_positive_float("Enter price: ")
        self.assertAlmostEqual(result, 12.50)
        self.assertEqual(mock_input.call_count, 3)
        printed_messages = [call.args[0] for call in mock_print.call_args_list]
        self.assertEqual(
            printed_messages,
            [
                "Please enter a valid number, e.g. 12.50",
                "Please enter a number greater than zero.",
            ],
        )

    @patch("builtins.print")
    def test_load_products_skips_bad_rows_and_loads_valid_rows(self, mock_print):
        csv_content = (
            "product_type, product_id,name, price, stock_quantity\n"
            "physical, P001, Desk Lamp, 25.00,10\n"
            "digital, D001, Photo Editor, 49.90,100\n"
            "service, S001, Installation, 30.00,5\n"
            "physical, P002, Office Chair, abc,3\n"
            "physical, P003, Monitor Stand, 39.50,7\n"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            inv = Inventory("Test Inventory")
            load_products(tmp_path, inv, self.supplier)
            self.assertEqual(len(inv.products), 3)
            self.assertEqual([p.product_id for p in inv.products], ["P001", "D001", "P003"])
            printed = [call.args[0] for call in mock_print.call_args_list]
            self.assertIn("3 products loaded.", printed)
            self.assertEqual(printed[-1], "Load attempt finished.")
        finally:
            os.remove(tmp_path)

    @patch("builtins.print")
    def test_load_products_missing_file_handled_gracefully(self, mock_print):
        inv = Inventory("Test Inventory")
        load_products("non_existent_products_file.csv", inv, self.supplier)
        self.assertEqual(len(inv.products), 0)
        printed = [call.args[0] for call in mock_print.call_args_list]
        self.assertEqual(
            printed,
            [
                "Products file not found: non_existent_products_file.csv",
                "Load attempt finished.",
            ],
        )


if __name__ == "__main__":
    unittest.main()
