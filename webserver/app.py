from flask import Flask
from waitress import serve
from flask import url_for, redirect

from webserver.api import rest_api


def register_blueprints(app, prefix):
    app.register_blueprint(rest_api, url_prefix=prefix)


def create_app(dictionary_with_strategies):
    """Creates a new Flask application and initialize application."""

    app = Flask(__name__, static_url_path='',
                static_folder='../dist',
                template_folder='../dist')

    @app.route('/')
    def home():
        return redirect(url_for('static', filename='index.html'))

    app.url_map.strict_slashes = False
    app.config['Strategies'] = dictionary_with_strategies
    register_blueprints(app, "/api")

    return app


def run(dictionary_with_strategies):
    serve(create_app(dictionary_with_strategies), host='0.0.0.0', port=8807)
