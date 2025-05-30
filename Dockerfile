FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory to /app/movbay (where manage.py lives)
WORKDIR /app/quickfiss_backend

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy gunicorn config (in project root)
COPY gunicorn_config.py /app/

# Copy movbay folder into /app/movbay
COPY quickfiss_backend/ /app/quickfiss_backend/

# Install Python dependencies (requirements.txt is inside movbay/)
RUN pip install --no-cache-dir -r requirements.txt

# Create static/media folders
RUN mkdir -p /app/quickfiss_backend/staticfiles /app/quickfiss_backend/media

# Collect static files


# Run gunicorn
CMD ["gunicorn", "--config", "/app/gunicorn_config.py", "quickfiss_backend.wsgi:application"]