from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")

    rentals = db.relationship("Rental", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price_per_day = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, default=1)
    image = db.Column(db.String(255))

    rentals = db.relationship("Rental", backref="product", lazy=True)

    def __repr__(self):
        return f"<Product {self.name}>"


class Rental(db.Model):
    __tablename__ = "rentals"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    total_price = db.Column(db.Integer, nullable=False)

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Rental {self.id}>"