# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports (FastAPI=8000, Streamlit=8501)
EXPOSE 8000 8501

# Run processes: FastAPI + Streamlit
CMD uvicorn api.app:app --host 0.0.0.0 --port 8000 & \
    streamlit run ui.py --server.port 8501 --server.address 0.0.0.0