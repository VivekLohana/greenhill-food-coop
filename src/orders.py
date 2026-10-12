
from src.products import is_valid_quantity


def validate_order(product, quantity):
    if product.withdrawn:
        return "Product is withdrawn"

    if not is_valid_quantity(product, quantity):
        return "Invalid quantity"

    if quantity == 0:
        return "Quantity must be greater than zero"

    return "Valid order"


def calculate_order_total(order_lines):
    total = 0

    for line in order_lines:
        total += line["unit_price"] * line["quantity"]

    return round(total, 2)


def confirm_order(order_lines):
    if not order_lines:
        return "Cannot confirm an empty order"

    total = calculate_order_total(order_lines)

    return {
        "status": "Confirmed",
        "items": len(order_lines),
        "total": total
    }
