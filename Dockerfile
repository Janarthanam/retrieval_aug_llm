# Use an official Python base image
FROM python:3.10-slim

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code into the container
COPY --chown=user run.sh api fe .

# Expose the port the app runs on
EXPOSE 8080

#todo these keys are environment specific
ENV OPENAI_API_KEY=zzz
ENV QDRANT_URL="https://32f125d3-5ab1-4058-a10a-bd38a1ebd647.us-east-1-0.aws.cloud.qdrant.io"
ENV STORE="QDRANT"
ENV be_url="http://127.0.0.1:8080"

# Start the application using Uvicorn
CMD ["/bin/sh", "./run.sh"]