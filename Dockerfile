# Dockerfile
FROM ubuntu:20.04

# Prevent timezone prompt during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libreoffice \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8080

# Start command
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

