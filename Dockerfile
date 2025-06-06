FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y portaudio19-dev gcc

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Change this if your app uses another main file
CMD ["python", "main.py"]
