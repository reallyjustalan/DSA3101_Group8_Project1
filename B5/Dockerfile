FROM python:3.7

# Set working directory
WORKDIR /app

# Expose port for Streamlit
EXPOSE 8080

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install -U pip && \
    pip install -r requirements.txt

# Copy the app files
COPY . .

# Run the Streamlit app
# Change app file accordingly 
ENTRYPOINT ["streamlit", "run", "Hello.py", "--server.port=8080", "--server.address=0.0.0.0"] 
