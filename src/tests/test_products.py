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
