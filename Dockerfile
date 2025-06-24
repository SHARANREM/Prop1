FROM python:3.11-slim

# Install LibreOffice and basic fonts
RUN apt-get update && \
    apt-get install -y libreoffice fonts-dejavu && \
    apt-get clean

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Start the app using gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
