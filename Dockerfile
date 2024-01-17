# Start your image with a node base image
FROM python:3-slim

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the app package and package-lock.json file
COPY src /src

# The /app directory should act as the main application directory
WORKDIR /src

# Start the app using serve commanD
CMD python manage.py runserver 0.0.0.0:8888