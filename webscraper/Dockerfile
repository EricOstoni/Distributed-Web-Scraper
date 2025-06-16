
FROM python:3.12-slim-bullseye AS build



WORKDIR /app


COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


COPY . /app


EXPOSE 6800


CMD ["scrapy", "list"]
