# ================
# SMART RESUME AGENT
# ================

FROM python:3.11-slim

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Gradio port
EXPOSE 7860

# Gradio runs on 0.0.0.0 by default
CMD ["python", "app.py"]
