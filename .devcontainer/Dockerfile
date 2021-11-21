FROM python:3.8.5-buster
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get update && apt-get install -y default-libmysqlclient-dev libgl1-mesa-dev nodejs curl
RUN python -m pip install -r /requirements.txt
COPY ./package.json /package.json
RUN npm install