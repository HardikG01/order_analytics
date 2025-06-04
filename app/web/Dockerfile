# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /usr/src/app
COPY . /app/

# Install Python dependencies
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --prefer-binary --no-cache-dir -r requirements.txt

# Run when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
