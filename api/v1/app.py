#!/usr/bin/python3
"""Module """

from models import storage
from api.v1.views import app_views
from flask import Flask
import os


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_session(exception=None):
    storage.close()


if __name__ == "__main__":
    """If it is main module"""

    HOST = os.environ.get("RG_API_HOST", "localhost")
    PORT = os.environ.get("RG_API_PORT", "5000")

    app.run(host=HOST, port=PORT, threaded=True)