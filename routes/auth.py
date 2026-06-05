from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User

bp_auth = Blueprint("auth", __name__)


@bp_auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing = User.query.filter_by(email=email).first()

        if existing:
            flash("Email sudah terdaftar", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            full_name=full_name,
            email=email,
            password_hash=generate_password_hash(password),
            role="user"
        )

        db.session.add(user)
        db.session.commit()

        flash("Registrasi berhasil, silakan login", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@bp_auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)

            if user.role == "admin":
                return redirect("/admin")

            return redirect("/dashboard")

        flash("Email atau password salah", "danger")

    return render_template("login.html")


@bp_auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Berhasil logout", "success")
    return redirect(url_for("auth.login"))