FROM python:3.12

# Set working directory
WORKDIR /app

# Expose port for Streamlit
EXPOSE 8501

RUN pip install uv
# Copy requirements and install dependencies
COPY requirements.txt ./

RUN uv pip install -U pip && \
    uv pip install -r requirements.txt && \
    uv pip install streamlit && \
    which streamlit && \
    python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')"

# Copy the app files
COPY . .

# Run the Streamlit app with the full path to streamlit
ENTRYPOINT ["python", "-m", "streamlit", "run", "Hello.py"]
