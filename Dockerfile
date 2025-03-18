FROM python:3.9-slim

# Install Rust and Git (required for dependencies)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add Rust to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV FLASK_PORT=8000
ENV PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 8000

# Run the application with gunicorn with proper logging
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-", "main:create_app()"]