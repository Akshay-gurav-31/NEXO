FROM python:3.11.11
# Install PortAudio dependencies
RUN apt-get update && apt-get install -y portaudio19-dev
# Upgrade pip and install requirements
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
# Copy project files
COPY . .
# Set Streamlit start command
CMD ["python", "-m", "streamlit", "run", "app.py"]
