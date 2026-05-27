FROM python:3.9-slim

WORKDIR /app

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y libgl1 libglx-mesa0 libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Copy backend code
COPY ./backend/ .

# Copy frontend files
COPY ./frontend/ ./frontend/

RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]