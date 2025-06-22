FROM python:3.11-slim

# Install system dependencies (LibreOffice)
RUN apt-get update && apt-get install -y libreoffice curl && apt-get clean

# Set work directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
