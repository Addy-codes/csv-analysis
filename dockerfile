# Use an official Python runtime as a parent image
FROM python:3.10-slim AS base

# Set environment variables to ensure Python runs in unbuffered mode and the output is logged to stdout/stderr
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create a directory for the app user
RUN mkdir -p /home/app

# Create an app user with no password and without a home directory
RUN adduser --disabled-password --gecos "" app

# Set the working directory to the app user's home directory
WORKDIR /home/app

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /home/app
COPY . .

# Change ownership of the application directory
RUN chown -R app:app /home/app

# Switch to the app user
USER app

# Expose the port that the app runs on
EXPOSE 8000

# Define an entrypoint command to run the app
ENTRYPOINT ["uvicorn"]

# Define the default command to run the app
CMD ["app.main:app", "--host", "0.0.0.0", "--port", "8000"]
