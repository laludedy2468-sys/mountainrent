from flask import Flask, redirect, url_for
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

from config import Config
from models import db, User, Product

from routes.auth import bp_auth
from routes.admin import bp_admin
from routes.user import bp_dashboard
from routes.rental import bp_rental


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprint
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_dashboard)
    app.register_blueprint(bp_rental)
    app.register_blueprint(bp_admin, url_prefix="/admin")

    @app.route("/")
    def home():
        return redirect(url_for("rental.products"))

    with app.app_context():

        db.create_all()

        # Produk awal
        if Product.query.count() == 0:

            db.session.add(Product(
                name="Tenda Eiger 4P",
                description="Tenda kapasitas 4 orang",
                price_per_day=50000,
                stock=5,
                image=""
            ))

            db.session.add(Product(
                name="Carrier Consina 60L",
                description="Tas carrier pendakian",
                price_per_day=35000,
                stock=4,
                image=""
            ))

            db.session.add(Product(
                name="Sleeping Bag",
                description="Sleeping bag hangat",
                price_per_day=15000,
                stock=10,
                image=""
            ))

            db.session.commit()

        # Admin default
        admin = User.query.filter_by(
            email=Config.DEFAULT_ADMIN_EMAIL
        ).first()

        if not admin:
            admin = User(
                full_name="Administrator",
                email=Config.DEFAULT_ADMIN_EMAIL,
                password_hash=generate_password_hash(
                    Config.DEFAULT_ADMIN_PASSWORD
                ),
                role="admin"
            )

            db.session.add(admin)
            db.session.commit()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )