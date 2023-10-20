# Stage 1: Build the application
FROM python:3.8 as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy your application code
COPY . /app

# Copy secrets.py from the host system into the image
COPY ./backend/secrets.py /app/backend/secrets.py

# Install dependencies and build the application
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py migrate

# Additional Dockerfile instructions for running your application
EXPOSE 8002

CMD ["python","manage.py","runserver","0.0.0.0:8002"] 