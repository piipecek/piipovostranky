import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail
from .helpers.check_files import check_logs_file
from .logs import log
from .paths import dotenv_path

db = SQLAlchemy()
cors = CORS()
mail = Mail()
login_manager = LoginManager()
load_dotenv(dotenv_path=dotenv_path(), verbose=True)


def create_app() -> Flask:
    check_logs_file()
    log("=== START appky ===")
    db_driver = os.environ.get("DB_DRIVER")
    db_username = os.environ.get("DB_USERNAME")
    db_password = os.environ.get("DB_PASSWORD")
    db_adress = os.environ.get("DB_ADRESS")
    db_name = os.environ.get("DB_NAME")
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"{db_driver}://{db_username}:{db_password}@{db_adress}/{db_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
    app.config["MAIL_PORT"] = "587"
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

    db.init_app(app)
    cors.init_app(app)
    mail.init_app(app)

    from .views.guest_views import guest_views
    from .views.auth_views import auth_views
    from .views.slovnik_views import slovnik_views
    from .views.visuals_views import visuals_views
    from .views.richard_views import richard_views
    from .views.sender_endpoints import sender
    from .views.admin_views import admin_views
    from .api.admin_api import admin_api
    from .api.guest_api import guest_api


    app.register_blueprint(guest_views, url_prefix="/")
    app.register_blueprint(auth_views, url_prefix="/auth")
    app.register_blueprint(slovnik_views, url_prefix="/slovnik")
    app.register_blueprint(visuals_views, url_prefix="/visuals")
    app.register_blueprint(richard_views, url_prefix="/api")
    app.register_blueprint(sender, url_prefix="/")
    app.register_blueprint(admin_views, url_prefix = "/admin")
    app.register_blueprint(admin_api, url_prefix = "/admin_api")
    app.register_blueprint(guest_api, url_prefix = "/guest_api")


    from .models.answer import Answer
    from .models.deck import Deck
    from .models.exam import Exam
    from .models.language import Language
    from .models.role import Role
    from .models.suggestion import Suggestion
    from .models.term import Term
    from .models.translation import Translation
    from .models.user import User
 
    with app.app_context():
        db.create_all()

    login_manager.login_view = "auth_views.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # get rovou kouka na primary key, nemusim delat filter_by(id=id)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("not_found.html"), 404

    @app.errorhandler(401)
    def not_authorised(e):
        return render_template("not_authorised.html"), 401

    return app