from src.products import Product, get_available_products, add_product, update_product, withdraw_product, is_valid_quantity, create_order_line
from src.products import Product, get_available_products, add_product, update_product


def test_available_products_are_returned():
    products = [
        Product("Oats", 3.40, "Round 33"),
        Product("Tahini", 9.80, "Round 33")
    ]

    result = get_available_products(products, "Round 33", True)

    assert len(result) == 2
    assert result[0].name == "Oats"
    assert result[1].name == "Tahini"


def test_withdrawn_products_are_not_returned():
    products = [
        Product("Oats", 3.40, "Round 33"),
        Product("Almonds", 16.88, "Round 33", withdrawn=True)
    ]

    result = get_available_products(products, "Round 33", True)

    assert len(result) == 1
    assert result[0].name == "Oats"

def test_message_when_round_is_closed():
    products = [
        Product("Oats", 3.40, "Round 33")
    ]

    result = get_available_products(products, "Round 33", False)

    assert result == "No open round"


def test_coordinator_can_add_product():
    products = []

    product = add_product(
        products,
        "Rice",
        4.50,
        "Round 33",
        True
    )

    assert len(products) == 1
    assert product.name == "Rice"
    assert product.price == 4.50


def test_coordinator_can_update_product():
    product = Product("Rice", 4.50, "Round 33")

    update_product(
        product,
        name="Brown Rice",
        price=4.80,
        is_coordinator=True
    )

    assert product.name == "Brown Rice"
    assert product.price == 4.80


def test_non_coordinator_cannot_add_product():
    products = []

    result = add_product(
        products,
        "Rice",
        4.50,
        "Round 33",
        False
    )

    assert result == "Permission denied"
    assert len(products) == 0


def test_non_coordinator_cannot_update_product():
    product = Product("Rice", 4.50, "Round 33")

    result = update_product(
        product,
        price=5.00,
        is_coordinator=False
    )

    assert result == "Permission denied"
    assert product.price == 4.50
def test_coordinator_can_withdraw_product():
    product = Product("Almonds", 16.88, "Round 33")

    result = withdraw_product(product, True)

    assert result.withdrawn is True


def test_withdrawn_product_is_not_available():
    product = Product("Almonds", 16.88, "Round 33")

    withdraw_product(product, True)

    result = get_available_products(
        [product],
        "Round 33",
        True
    )

    assert len(result) == 0


def test_non_coordinator_cannot_withdraw_product():
    product = Product("Almonds", 16.88, "Round 33")

    result = withdraw_product(product, False)

    assert result == "Permission denied"
    assert product.withdrawn is False

def test_product_stores_per_unit_sale_type():
    product = Product("Tahini", 9.80, "Round 33", sale_type="Per Unit")
    assert product.sale_type == "Per Unit"


def test_product_stores_per_kilogram_sale_type():
    product = Product("Oats", 3.40, "Round 33", sale_type="Per Kilogram")
    assert product.sale_type == "Per Kilogram"


def test_per_unit_product_accepts_whole_number():
    product = Product("Tahini", 9.80, "Round 33", sale_type="Per Unit")
    assert is_valid_quantity(product, 2) is True


def test_per_unit_product_rejects_decimal_quantity():
    product = Product("Tahini", 9.80, "Round 33", sale_type="Per Unit")
    assert is_valid_quantity(product, 1.5) is False


def test_per_kilogram_product_accepts_decimal_quantity():
    product = Product("Oats", 3.40, "Round 33", sale_type="Per Kilogram")
    assert is_valid_quantity(product, 1.5) is True

def test_order_line_stores_product_price():
    product = Product("Oats", 3.40, "Round 33", sale_type="Per Kilogram")

    order_line = create_order_line(product, 2)

    assert order_line["unit_price"] == 3.40
    assert order_line["quantity"] == 2


def test_historical_price_does_not_change_when_product_price_changes():
    product = Product("Oats", 3.40, "Round 33", sale_type="Per Kilogram")

    order_line = create_order_line(product, 2)

    product.price = 4.20

    assert product.price == 4.20
    assert order_line["unit_price"] == 3.40


def test_historical_order_total_remains_based_on_original_price():
    product = Product("Oats", 3.40, "Round 33", sale_type="Per Kilogram")

    order_line = create_order_line(product, 2)
    original_total = order_line["unit_price"] * order_line["quantity"]

    product.price = 4.20
    historical_total = order_line["unit_price"] * order_line["quantity"]

    assert original_total == 6.80
    assert historical_total == 6.80
