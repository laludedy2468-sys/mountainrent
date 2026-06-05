from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import Rental, Product

bp_dashboard = Blueprint("dashboard", __name__)


@bp_dashboard.route("/dashboard")
@login_required
def dashboard():

    rentals = Rental.query.filter_by(
        user_id=current_user.id
    ).all()

    products = Product.query.all()

    return render_template(
        "user/dashboard.html",
        user=current_user,
        rentals=rentals,
        products=products
    )


@bp_dashboard.route("/profile")
@login_required
def profile():

    rentals = Rental.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "user/profile.html",
        user=current_user,
        rentals=rentals
    )


@bp_dashboard.route("/history")
@login_required
def history():

    rentals = Rental.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "user/history.html",
        rentals=rentals
    )