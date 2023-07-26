# Use an official Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code into the container
COPY api .

# Expose the port the app runs on
EXPOSE 8080

#todo these keys are environment specific
ENV OPENAI_API_KEY=zzz
ENV QDRANT_URL="https://32f125d3-5ab1-4058-a10a-bd38a1ebd647.us-east-1-0.aws.cloud.qdrant.io"
ENV STORE="QDRANT"
# Start the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]