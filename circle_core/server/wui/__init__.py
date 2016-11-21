"""WebUI."""

from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    """仮."""
    return 'Greetings from flask!'


def create_app():
    """App factory."""
    # TODO: Use blueprint
    return app
