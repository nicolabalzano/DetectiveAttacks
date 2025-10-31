# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /vuln_score

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port the app runs on
EXPOSE 5004

# Set environment variable for Flask
ENV FLASK_APP=controller/Controller.py
ENV PYTHONUNBUFFERED=1
ENV PORT=5004
ENV PYTHONPATH=/vuln_score

# Run the application
CMD ["python", "controller/Controller.py"]
