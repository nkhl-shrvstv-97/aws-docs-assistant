FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uvicorn

# Copy all application files into a 'backend' subdirectory
COPY . ./backend

# Expose port 8000
EXPOSE 8000

# Set Python path and unbuffered logging
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Start FastAPI application
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
