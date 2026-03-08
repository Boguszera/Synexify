# ===========================================================================
# Dockerfile for production server
# ===========================================================================

# python base image
FROM python:3.12-slim

# psycopg2 dependencies + psql client
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy configuration files
COPY pyproject.toml ./

# install project dependecies (production)
RUN pip install --upgrade pip \
    && pip install --no-cache-dir .

# copy source code
COPY . .

EXPOSE 8000

# default command (can be overridden by docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "appcore.wsgi:application"]
