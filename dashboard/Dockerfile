FROM python:3.11-slim

# Install system dependencies for Postgres
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project
COPY . .

# Set the environment variable explicitly
ENV DJANGO_SETTINGS_MODULE=core.settings

# Expose port
EXPOSE 8000

# Use the 'sh -c' approach to ensure the environment variables are loaded
CMD ["sh", "-c", "daphne -b 0.0.0.0 -p 8000 core.asgi:application"]