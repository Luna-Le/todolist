FROM python:3.12

# Set the working directory
WORKDIR /code

# Install netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Copy the migration script into the container
COPY run_migrations.sh .

# Make the migration script executable
RUN chmod +x run_migrations.sh

# Start the application and run migrations
CMD ["sh", "-c", "./run_migrations.sh && uvicorn app.main:app --host 0.0.0.0 --port 80"]