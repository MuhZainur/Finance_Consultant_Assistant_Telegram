# Base Image: Lightweight Python
FROM python:3.10-slim

# Set Working Directory
WORKDIR /app

# Prevent Python from buffering stdout/stderr (better logs)
ENV PYTHONUNBUFFERED=1

# Install Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project Files
COPY . .

# Expose Port (Standard for Cloud Run)
EXPOSE 8080

# Command to Run FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
