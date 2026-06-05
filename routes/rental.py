from datetime import datetime

from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user

from models import db, Product, Rental

bp_rental = Blueprint("rental", __name__)


@bp_rental.route("/products")
def products():

    products = Product.query.all()

    return render_template(
        "rental/products.html",
        products=products
    )


@bp_rental.route("/rent/<int:product_id>", methods=["GET", "POST"])
@login_required
def rent_product(product_id):

    product = Product.query.get_or_404(product_id)

    if request.method == "POST":

        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        days = (end - start).days

        if days <= 0:
            flash(
                "Tanggal kembali harus lebih besar dari tanggal sewa",
                "danger"
            )
            return redirect(request.url)

        total_price = days * product.price_per_day

        rental = Rental(
            user_id=current_user.id,
            product_id=product.id,
            start_date=start.date(),
            end_date=end.date(),
            total_price=total_price,
            status="Pending"
        )

        db.session.add(rental)
        db.session.commit()

        flash(
            "Penyewaan berhasil diajukan",
            "success"
        )

        return redirect("/dashboard")

    return render_template(
        "rental/detail.html",
        product=product
    )