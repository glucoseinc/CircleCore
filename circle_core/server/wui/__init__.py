from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
  return 'Greetings from flask!'


def create_app():
  # TODO: Use blueprint
  return app
