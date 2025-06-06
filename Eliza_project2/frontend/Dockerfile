FROM python:3.11-slim

# Install portaudio dev library for PyAudio
RUN apt-get update && apt-get install -y portaudio19-dev

WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of your app code
COPY . .

CMD ["python", "app.py"]   # Apne main script ka naam yahan dalna
