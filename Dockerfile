FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y portaudio19-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python packages
RUN pip install --upgrade pip --root-user-action=ignore
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Expose port (informational, Render uses $PORT)
EXPOSE 5000

# Run Flask app with gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT main:app
