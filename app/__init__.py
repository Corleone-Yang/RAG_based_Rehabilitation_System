from flask import Flask
from app.routes import routes
from app.models import short_term_memory, long_term_memory, dynamic_memory
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)  # used for flash and session

    # Initialize memory objects
    app.stm = short_term_memory()
    app.ltm = long_term_memory()
    app.dm = dynamic_memory()
    app.match = []

    # Initialize blueprint
    app.register_blueprint(routes)

    return app
