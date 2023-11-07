FROM python:3.11-slim-buster

#EXPOSE 8000

COPY . /app
RUN pip install --upgrade pip
RUN pip install -r app/requirements.txt
WORKDIR /app
