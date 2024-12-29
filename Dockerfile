# Use a Python image as a base
FROM python:3.8-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents to the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 8000 for the app
EXPOSE 8000

# Run the Django server when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
