# Use an official Python image as a base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV WORKDIR=/app

# Set working directory
WORKDIR $WORKDIR

# Copy application files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy secrets from .env file
COPY .env .env

# Expose the required ports
EXPOSE 8000 8501

# Command to run both FastAPI and Streamlit using process manager
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --reload & streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]