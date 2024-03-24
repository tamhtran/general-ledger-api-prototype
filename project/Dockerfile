# pull official base image
FROM python:3.11.2-slim-buster

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# set environment variables
#PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
#PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc\
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# add entrypoint.sh for postgres db
COPY ./entrypoint.sh .

RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh to make sure postgres is up and running
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]