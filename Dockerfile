FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Expose the port FastAPI runs on
EXPOSE 7500

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7500"]
