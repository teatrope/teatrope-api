FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential default-libmysqlclient-dev pkg-config && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . /code

EXPOSE $PORT

ENTRYPOINT ["sh", "/code/docker/entrypoints/entrypoint.sh"]  # Add this to run entrypoint.sh on startup
CMD gunicorn --bind 0.0.0.0:$PORT teatrope.wsgi:application