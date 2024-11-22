# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container and install the dependencies
COPY requirements.txt /app/
RUN  pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container at /app
COPY . /app/

# Running static
RUN ls -la /app/static

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000 for the Django development server
EXPOSE 8000

# Run the command to start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
