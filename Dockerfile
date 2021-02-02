# pull official base image
FROM python:3.6

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /app

RUN chmod +x /app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["sh", "/app/entrypoint.sh"]