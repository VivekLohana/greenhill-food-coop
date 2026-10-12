
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

from src.orders import (
    edit_order_item,
    remove_order_item,
    cancel_order,
    get_order_status,
    get_order_summary,
    get_order_history
)


def test_edit_order_item():
    lines = [{"product_name": "Oats", "unit_price": 3.40, "quantity": 2}]

    result = edit_order_item(lines, "Oats", 3)

    assert result == "Order item updated"
    assert lines[0]["quantity"] == 3


def test_edit_order_item_invalid_quantity():
    lines = [{"product_name": "Oats", "unit_price": 3.40, "quantity": 2}]

    result = edit_order_item(lines, "Oats", 0)

    assert result == "Invalid quantity"
    assert lines[0]["quantity"] == 2


def test_remove_order_item():
    lines = [{"product_name": "Oats", "unit_price": 3.40, "quantity": 2}]

    result = remove_order_item(lines, "Oats")

    assert result == "Order item removed"
    assert len(lines) == 0


def test_cancel_order():
    order = {"status": "Confirmed", "items": 1, "total": 6.80}

    result = cancel_order(order)

    assert result["status"] == "Cancelled"


def test_get_order_status():
    order = {"status": "Confirmed"}

    assert get_order_status(order) == "Confirmed"


def test_get_order_summary():
    lines = [{"product_name": "Oats", "unit_price": 3.40, "quantity": 2}]

    result = get_order_summary(lines)

    assert result["items"] == 1
    assert result["total"] == 6.80
    assert result["products"][0]["product_name"] == "Oats"


def test_get_order_history():
    orders = [
        {"status": "Confirmed", "total": 6.80},
        {"status": "Pending", "total": 3.40},
        {"status": "Cancelled", "total": 9.80}
    ]

    result = get_order_history(orders)

    assert len(result) == 2
    assert result[0]["status"] == "Confirmed"
    assert result[1]["status"] == "Cancelled"