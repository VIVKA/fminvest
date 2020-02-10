import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_worker(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        os.getenv('DATABASE_URL', 'postgresql://localhost/factota')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

    db.init_app(app)

    return app


def create_app(config=None):
    app = Flask(
        __name__,
        static_folder='./static',
        static_url_path='/static')

    # app.config['ENVIRONMENT'] = \
    #     os.getenv('FLASK_CONFIG', 'development')

    # app.config['TEMPLATES_AUTO_RELOAD'] = True

    # app.config['BASIC_AUTH_USERNAME'] = 'username'
    # app.config['BASIC_AUTH_PASSWORD'] = 'password'

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        os.getenv('DATABASE_URL', 'postgresql://localhost/factota')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

    # if app.config['ENVIRONMENT'] != 'development':
    #     SSLify(app)

    db.init_app(app)

    from app.blueprint import view
    app.register_blueprint(view)

    # app.secret_key = 'xBXyz4eGfRNMN5NpeaIzFU12AW98Nvs5'

    # @app.errorhandler(404)
    # def not_found(e):
    #     return render_template('errors/not_found.html')

    from app.utils import utils

    @app.before_first_request
    def before_requests():
        utils.warm_caches()

    return app
