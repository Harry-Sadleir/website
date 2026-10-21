import os
import secrets
from pathlib import Path
from flask import Flask
from .helpers import secure_headers, add_noindex_header
from .routes import bp as main_bp

def create_app():
    app = Flask(__name__)

    # Real key comes from /etc/woof-site.env on the Pi (systemd EnvironmentFile).
    # ponytail: random fallback keeps local dev and the deploy script's import check
    # working; if SECRET_KEY is ever missing in prod, each gunicorn worker gets its own key.
    app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

    # blueprints
    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_asset_ver():
        try:
            css = Path(app.static_folder) / "style.css"
            ver = int(css.stat().st_mtime)
        except Exception:
            ver = 0
        return {"ASSET_VER": ver}

    # security headers
    app.after_request(secure_headers)
    app.after_request(add_noindex_header)
    # client side cache
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 60 * 60 * 24 * 7  # 7 days

    return app

# optional: allow `flask --app woof_site run` in dev
app = create_app()