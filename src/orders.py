
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
def edit_order_item(order_lines, product_name, new_quantity):
    if new_quantity <= 0:
        return "Invalid quantity"

    for line in order_lines:
        if line["product_name"] == product_name:
            line["quantity"] = new_quantity
            return "Order item updated"

    return "Product not found"


def remove_order_item(order_lines, product_name):
    for line in order_lines:
        if line["product_name"] == product_name:
            order_lines.remove(line)
            return "Order item removed"

    return "Product not found"


def cancel_order(order):
    if order["status"] == "Cancelled":
        return "Order already cancelled"

    order["status"] = "Cancelled"
    return order


def get_order_status(order):
    return order["status"]


def get_order_summary(order_lines):
    return {
        "items": len(order_lines),
        "total": calculate_order_total(order_lines),
        "products": order_lines.copy()
    }


def get_order_history(orders):
    return [
        order for order in orders
        if order["status"] in ("Confirmed", "Cancelled")
    ]