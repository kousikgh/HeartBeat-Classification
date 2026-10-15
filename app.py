"""Flask application entry point for the academic ECG classification prototype."""

from __future__ import annotations

from flask import Flask, jsonify

from config import Config
from src.database import init_db
from src.web.routes import web


def create_app(test_config: dict[str, object] | None = None) -> Flask:
    """Create and configure the local Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config is not None:
        app.config.update(test_config)
    app.register_blueprint(web)

    with app.app_context():
        init_db()

    @app.errorhandler(413)
    def upload_too_large(_error):
        return jsonify(error="Upload is too large. The maximum file size is 5 MB."), 413

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
