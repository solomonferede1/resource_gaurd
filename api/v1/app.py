#!/usr/bin/python3
"""Module """

from models import storage
from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS
import os


app = Flask(__name__)


app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_session(exception=None):
    storage.close()


if __name__ == "__main__":
    """If it is main module"""

    HOST = os.environ.get("RG_API_HOST", "localhost")
    PORT = os.environ.get("RG_API_PORT", "5000")

    app.run(host=HOST, port=PORT, threaded=True)