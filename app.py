import os

from flask import Flask, render_template

from src.products import Product, get_available_products


app = Flask(__name__)

CURRENT_ROUND = "Round 33"

products = [
    Product(
        "Oats",
        3.40,
        CURRENT_ROUND,
        sale_type="Per Kilogram"
    ),
    Product(
        "Tahini",
        9.80,
        CURRENT_ROUND,
        sale_type="Per Unit"
    ),
    Product(
        "Almonds",
        16.88,
        CURRENT_ROUND,
        sale_type="Per Kilogram"
    ),
    Product(
        "Olive Oil",
        18.50,
        CURRENT_ROUND,
        sale_type="Per Unit"
    )
]


@app.route("/")
def home():
    available_products = get_available_products(
        products,
        CURRENT_ROUND,
        True
    )

    if isinstance(available_products, str):
        return render_template(
            "index.html",
            products=[],
            current_round=CURRENT_ROUND,
            message=available_products
        )

    return render_template(
        "index.html",
        products=available_products,
        current_round=CURRENT_ROUND,
        message=None
    )


@app.route("/health")
def health():
    return {
        "status": "ok",
        "application": "Greenhill Food Co-op"
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
