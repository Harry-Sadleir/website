# woof-site

Personal portfolio (Flask 3). One-page layout with projects and recent posts grabbed from placeholder substack.

## Quick start
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python run.py
# http://127.0.0.1:5000
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
- [ ] Rate-limit at Caddy/Nginx (e.g., 10 r/s per IP).

### Data / Integrations
- [X] Substack RSS fetch: keep 24h cache; timeout 8s.
- [X] Add a “Current project” section
- [ ] Fix “Collections” properly - sources/notes; archive to Substack when done.

### SEO
- [X] Investigate whether to allow indexing (robots.txt + X-Robots-Tag).
- [X] Fix sitemap

### Code cleanup
- [X] Set up app factory + blueprints (`routes.py`, `helpers.py`, `data/`).
- [X] Add basic tests for helpers (Substack parsing, reading loader).

### Deployment
- [X] Gunicorn + Caddy on Raspberry Pi.
- [X] Systemd service with `Environment=SECRET_KEY=...`.
- [X] HTTPS, HSTS, compression, and static caching.
- [X] Git deploy script to update `static/` + restart service.
