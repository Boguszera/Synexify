# python base image
FROM python:3.12-slim

# psycopg2 dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# copy project files
COPY . .

# run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
