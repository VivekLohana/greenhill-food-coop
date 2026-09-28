class Product:
    def __init__(self, name, price, round_name, withdrawn=False, sale_type="Per Unit"):
        self.name = name
        self.price = price
        self.round_name = round_name
        self.withdrawn = withdrawn
        self.sale_type = sale_type


def get_available_products(products, current_round, round_open):
    if not round_open:
        return "No open round"

    available_products = []

    for product in products:
        if product.round_name == current_round and not product.withdrawn:
            available_products.append(product)

    return available_products
def add_product(products, name, price, round_name, is_coordinator):
    if not is_coordinator:
        return "Permission denied"

    product = Product(name, price, round_name)
    products.append(product)
    return product


def update_product(product, name=None, price=None, is_coordinator=False):
    if not is_coordinator:
        return "Permission denied"

    if name is not None:
        product.name = name

    if price is not None:
        product.price = price

    return product
    
def withdraw_product(product, is_coordinator):
    if not is_coordinator:
        return "Permission denied"

    product.withdrawn = True
    return product
def is_valid_quantity(product, quantity):
    if product.sale_type == "Per Unit":
        return isinstance(quantity, int) and quantity >= 0

    if product.sale_type == "Per Kilogram":
        return isinstance(quantity, (int, float)) and quantity >= 0

    return False
    
def create_order_line(product, quantity):
    return {
        "product_name": product.name,
        "unit_price": product.price,
        "quantity": quantity
    }
