# Use Python 3.10 image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy only requirements first (to leverage Docker layer caching)
COPY requirements.txt .

# Install dependencies first (before copying rest of the code)
RUN pip install -r requirements.txt

# Now copy the rest of the application files
COPY . .

# Expose the application port
EXPOSE 8000

# Command to start the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
