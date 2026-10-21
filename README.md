# woof-site

Personal portfolio (Flask 3). One-page layout with projects and recent Substack posts, plus the Quest Log app at `/quest-log`.

## Quick start
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python run.py
# http://127.0.0.1:5000

python -m unittest   # tests
```


## TODO / Ideas

### Content
- [x] Replace placeholder project text/images with final content.
- [x] Point `SUBSTACK_BASE` to my own Substack.

### Design / UX
- [x] Light hover animation for project cards (already there, tune).
- [ ] Add tags (e.g., Python, Flask, Security) under titles, maybe just do this on substack tbh

### Performance
- [x] Convert all project PNG/JPG to WebP (keep PNG/JPG fallback).
- [x] Keep hero image preloaded and sized (LCP check in Lighthouse).
- [x] Set asset version to CSS mtime in dev; use git hash in prod.

### Security
- [x] Turn off `DEBUG` in production; run via gunicorn.
- [x] Set `SECRET_KEY` via environment variable on the Pi.
- [x] Check security headers (current: CSP, XFO, XCTO, Referrer-Policy).
- [ ] Rate-limit at Cloudflare (e.g., 10 r/s per IP).

### Data / Integrations
- [X] Substack RSS fetch: keep 24h cache; timeout 8s.
- [X] Add a “Current project” section
- [ ] Fix “Collections” properly - sources/notes; archive to Substack when done.

### SEO
- [X] Investigate whether to allow indexing (robots.txt + X-Robots-Tag).
- [X] Fix sitemap

### Code cleanup
- [X] Set up app factory + blueprints (`routes.py`, `helpers.py`, `data/`).
- [X] Tests for the Substack/GitHub caching and feed parsing (`tests/`).

### Deployment
- [X] Gunicorn on the Raspberry Pi, behind a Cloudflare tunnel.
- [X] Systemd service; `SECRET_KEY` comes from `/etc/woof-site.env` (root-only).
- [X] HTTPS, compression, and static caching.
- [ ] HSTS: Cloudflare currently sends `max-age=0` (off); turn on in SSL/TLS → Edge Certificates.
- [X] Git deploy script to update `static/` + restart service.
