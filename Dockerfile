# Infrared app image (Flask + gunicorn). Stateless: Solr and the image repos
# are external (a Solr container and a mounted volume) — see docker-compose.yml.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install deps first for better layer caching.
COPY pyproject.toml ./
COPY infrared ./infrared
COPY wsgi.py ./
# Editable install keeps the package rooted at /app so it finds static/, about/,
# and configs/ at runtime (relative to the package).
RUN pip install -e ".[deploy]"

# App assets and config (the 90 GB image repos are NOT baked in — they are a
# mounted volume served by the reverse proxy).
COPY static ./static
COPY about ./about
COPY configs ./configs

EXPOSE 8000

# Multi-tenant by default: wsgi.py calls create_app(), which reads INFRARED_SITES.
# For a single-core container instead, set INFRARED_CORE and drop INFRARED_SITES.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60", "wsgi:app"]
