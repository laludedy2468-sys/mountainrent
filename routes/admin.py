from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from models import db, User, Product, Rental

bp_admin = Blueprint("admin", __name__)


def admin_only():
    return current_user.is_authenticated and current_user.role == "admin"


@bp_admin.route("/")
@login_required
def admin_dashboard():

    if not admin_only():
        return "Akses ditolak", 403

    total_users = User.query.count()
    total_products = Product.query.count()
    total_rentals = Rental.query.count()

    total_income = sum(
        rental.total_price or 0
        for rental in Rental.query.all()
    )

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_products=total_products,
        total_rentals=total_rentals,
        total_income=total_income
    )


# ==========================
# PRODUK
# ==========================

@bp_admin.route("/products")
@login_required
def products():

    if not admin_only():
        return "Akses ditolak", 403

    products = Product.query.all()

    return render_template(
        "admin/products.html",
        products=products
    )


@bp_admin.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():

    if not admin_only():
        return "Akses ditolak", 403

    if request.method == "POST":

        image_file = request.files["image"]

        filename = ""

        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)

            upload_folder = os.path.join(
                "static",
                "uploads"
            )

            os.makedirs(upload_folder, exist_ok=True)

            image_file.save(
                os.path.join(
                    upload_folder,
                    filename
                )
            )

        product = Product(
            name=request.form["name"],
            description=request.form["description"],
            price_per_day=int(request.form["price_per_day"]),
            stock=int(request.form["stock"]),
            image=filename
        )

        db.session.add(product)
        db.session.commit()

        flash(
            "Produk berhasil ditambahkan",
            "success"
        )

        return redirect("/admin/products")

    return render_template(
        "admin/product_form.html"
    )

@bp_admin.route("/products/delete/<int:id>")
@login_required
def delete_product(id):

    if not admin_only():
        return "Akses ditolak", 403

    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    flash("Produk berhasil dihapus", "success")

    return redirect("/admin/products")


# ==========================
# USER
# ==========================

@bp_admin.route("/users")
@login_required
def users():

    if not admin_only():
        return "Akses ditolak", 403

    users = User.query.all()

    return render_template(
        "admin/users.html",
        users=users
    )


# ==========================
# RENTAL
# ==========================

@bp_admin.route("/rentals")
@login_required
def rentals():

    if not admin_only():
        return "Akses ditolak", 403

    rentals = Rental.query.all()

    return render_template(
        "admin/rentals.html",
        rentals=rentals
    )


@bp_admin.route("/rental/approve/<int:id>")
@login_required
def approve_rental(id):

    if not admin_only():
        return "Akses ditolak", 403

    rental = Rental.query.get_or_404(id)

    rental.status = "Disetujui"

    db.session.commit()

    return redirect("/admin/rentals")


@bp_admin.route("/rental/reject/<int:id>")
@login_required
def reject_rental(id):

    if not admin_only():
        return "Akses ditolak", 403

    rental = Rental.query.get_or_404(id)

    rental.status = "Ditolak"

    db.session.commit()

    return redirect("/admin/rentals")