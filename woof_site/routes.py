from flask import Blueprint, render_template, url_for, Response, request, jsonify
from pathlib import Path
from datetime import datetime, timezone
from .github_activity import get_github_activity
import markdown
from weasyprint import HTML, CSS

from .helpers import (
    fetch_recent_from_substack,
    load_reading,
    SUBSTACK_BASE,
)
from .data.projects import PROJECTS

bp = Blueprint("main", __name__)

BASE_DIR = Path(__file__).resolve().parent

# warm the Substack cache once per process (Flask 3 safe)
_warmed = False
@bp.before_app_request
def _warm_cache_once():
    global _warmed
    if _warmed:
        return
    try:
        fetch_recent_from_substack(limit=5)
    except Exception:
        pass
    _warmed = True

def _iso_date(p: Path) -> str:
    try:
        t = p.stat().st_mtime
        return datetime.fromtimestamp(t, tz=timezone.utc).date().isoformat()
    except Exception:
        return datetime.now(timezone.utc).date().isoformat()

@bp.route("/")
def index():
    reading = load_reading()

    return render_template(
        "index.html",
        projects=PROJECTS,                                  # manual key projects
        posts=fetch_recent_from_substack(limit=5),          # Substack recent
        reading=reading,
        title="woofdog",
        substack_base=SUBSTACK_BASE,
        activity = get_github_activity(limit=5)

    )

@bp.route("/CL")
def CL():
    return render_template("CL.html")

@bp.route("/render-markdown-preview", methods=["POST"])
def render_markdown_preview():
    data = request.get_json()
    markdown_text = data.get("markdown", "")
    html_content = markdown.markdown(markdown_text, extensions=['extra'])
    return jsonify({"html": html_content})

@bp.route("/download-pdf", methods=["POST"])
def download_pdf():
    markdown_text = request.form.get("markdown", "")
    html_content = markdown.markdown(markdown_text, extensions=['extra'])

    pdf_css = """
    @import url('https://fonts.googleapis.com/css2?family=Garamond:wght@400;700&display=swap');

    @page { size: A4; margin: 2cm; }
    body { font-family: sans-serif; }
    pre { background-color: #eee; padding: 1em; }
    code { font-family: monospace; }
    
    h1 {
        font-family: 'Garamond', serif;
        font-size: 22px;
        font-weight: bold;
        margin: 0;
        text-align: center;
    }

    h1 + p {
        font-family: 'Garamond', serif;
        font-size: 13px;
        margin: 5px 0;
        text-align: center;
    }
    p {
        font-family: 'Garamond', serif;
        font-size: 13px;
        line-height: 1.6;
    }

    hr {
        border: 0;
        border-top: 1px solid #ccc;
        margin: 10px auto;
        width: 100%;
    }
    """

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Document</title>
        <style>{pdf_css}</style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    pdf = HTML(string=full_html).write_pdf()

    return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment;filename=document.pdf"}
    )

@bp.route("/sitemap.xml")
def sitemap():
    pages = [
        {
            "loc": url_for("main.index", _external=True),
            "lastmod": _iso_date(BASE_DIR / "templates" / "index.html"),
        },
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        xml.append("<url>")
        xml.append(f"  <loc>{p['loc']}</loc>")
        xml.append(f"  <lastmod>{p['lastmod']}</lastmod>")
        xml.append("</url>")
    xml.append("</urlset>")
    return Response("\n".join(xml), mimetype="application/xml")

@bp.route("/robots.txt")
def robots():
    # Disallow crawlers for now
    return Response("User-agent: *\nDisallow: /\n", mimetype="text/plain")
