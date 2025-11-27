FROM manimcommunity/manim:latest

USER root

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app
WORKDIR /app

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
