from src. products import Product, get_available_products


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
