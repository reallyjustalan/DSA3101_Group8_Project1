# Start from lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY requirements.txt .
COPY app.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the app (with explicit host/port for Docker)
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
