class Product:
    def __init__(self, name, price, round_name, withdrawn=False):
        self.name = name
        self.price = price
        self.round_name = round_name
        self.withdrawn = withdrawn


def get_available_products(products, current_round, round_open):
    if not round_open:
        return "No open round"

    available_products = []

    for product in products:
        if product.round_name == current_round and not product.withdrawn:
            available_products.append(product)

    return available_products
