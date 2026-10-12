
from src.products import Product, create_order_line
from src.orders import validate_order, calculate_order_total, confirm_order


def test_valid_order():
    product = Product("Oats", 3.40, "Round 33", sale_type="Per Kilogram")
    assert validate_order(product, 2) == "Valid order"


def test_invalid_quantity():
    product = Product("Tahini", 9.80, "Round 33", sale_type="Per Unit")
    assert validate_order(product, 1.5) == "Invalid quantity"


def test_zero_quantity():
    product = Product("Oats", 3.40, "Round 33")
    assert validate_order(product, 0) == "Quantity must be greater than zero"


def test_withdrawn_product():
    product = Product("Oats", 3.40, "Round 33", withdrawn=True)
    assert validate_order(product, 2) == "Product is withdrawn"


def test_order_total():
    oats = Product("Oats", 3.40, "Round 33")
    tahini = Product("Tahini", 9.80, "Round 33")

    lines = [
        create_order_line(oats, 2),
        create_order_line(tahini, 1)
    ]

    assert calculate_order_total(lines) == 16.60


def test_confirm_order():
    product = Product("Oats", 3.40, "Round 33")
    lines = [create_order_line(product, 2)]

    result = confirm_order(lines)

    assert result["status"] == "Confirmed"
    assert result["items"] == 1
    assert result["total"] == 6.80


def test_empty_order():
    assert confirm_order([]) == "Cannot confirm an empty order"
