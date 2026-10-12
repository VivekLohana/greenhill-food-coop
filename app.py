
import os

from flask import Flask, render_template, request, redirect, url_for

from src.products import Product, get_available_products
from src.members import (
    register_member,
    search_members,
    get_member,
    update_member,
    activate_member,
    deactivate_member
)
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

members = []


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


@app.route("/history")
def order_history():
    from src.products import create_order_line

    product = products[0]
    order_line = create_order_line(product, 2)

    original_price = order_line["unit_price"]

    return render_template(
        "history.html",
        order_line=order_line,
        total=original_price * order_line["quantity"]
    )


@app.route("/health")
def health():
    return {
        "status": "ok",
        "application": "Greenhill Food Co-op"
    }


@app.route("/members")
def member_list():
    search_query = request.args.get("search", "").strip()

    if search_query:
        displayed_members = search_members(
            members,
            search_query
        )
    else:
        displayed_members = members

    return render_template(
        "members.html",
        members=displayed_members,
        message=None,
        search_query=search_query
    )


@app.route("/members/register", methods=["POST"])
def member_register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()

    next_id = max(
        (member.member_id for member in members),
        default=0
    ) + 1

    result = register_member(
        members,
        next_id,
        name,
        email,
        phone
    )

    if isinstance(result, str):
        return render_template(
            "members.html",
            members=members,
            message=result,
            search_query=""
        ), 400

    return redirect(url_for("member_list"))


@app.route("/members/<int:member_id>/edit", methods=["GET", "POST"])
def member_edit(member_id):
    member = get_member(members, member_id)

    if member is None:
        return "Member not found", 404

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        result = update_member(
            members, member_id, name, email, phone
        )

        if isinstance(result, str):
            return render_template(
                "edit_member.html",
                member=member,
                message=result
            ), 400

        return redirect(url_for("member_list"))

    return render_template(
        "edit_member.html",
        member=member,
        message=None
    )


@app.route("/members/<int:member_id>/deactivate", methods=["POST"])
def member_deactivate(member_id):
    member = get_member(members, member_id)

    if member is None:
        return "Member not found", 404

    deactivate_member(members, member_id)

    return redirect(url_for("member_list"))


@app.route("/members/<int:member_id>/activate", methods=["POST"])
def member_activate(member_id):
    member = get_member(members, member_id)

    if member is None:
        return "Member not found", 404

    activate_member(members, member_id)

    return redirect(url_for("member_list"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
