# Stage 1: Build the application
FROM python:3.8 as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies and build the application
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# static files 
RUN python manage.py collectstatic --noinput

RUN python manage.py migrate

# Stage 2: Create a lightweight production image
#FROM python:3.8-slim

#WORKDIR /app

# Copy the dependencies and static files from the builder stage
#COPY --from=builder /app /app

# Install dependencies and build the application
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

# PORT
EXPOSE 8002

#CMD ["python","manage.py","runserver","0.0.0.0:8002"] 

# use gunicorn to run application
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8002"] 