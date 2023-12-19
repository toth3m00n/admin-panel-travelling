import os
from flask import Flask
from sqlalchemy import text

from .hotel.models import *
from .client.models import *
from .class_type.models import *
from .convenience.models import *


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ.get('APP_SETTINGS'))

    db.init_app(app)

    with app.app_context():
        db.create_all()

        with app.open_resource("table/trigger.sql") as f:
            trigger_sql = f.read().decode("utf-8")
            db.session.execute(text(trigger_sql))

        db.session.commit()

    from app.homepage.index import index_bp
    app.register_blueprint(index_bp, url_prefix='')

    from app.client.client import client_bp
    app.register_blueprint(client_bp, url_prefix='/client')

    from app.hotel.hotel import hotel_bp
    app.register_blueprint(hotel_bp, url_prefix='/hotel')

    return app

