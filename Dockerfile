FROM python:3.8.5-buster
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt
RUN apt-get update && apt-get install -y npm curl
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN python -m pip install -r /requirements.txt
COPY ./package.json /bramsplanter/frontend/package.json
RUN npm i npm@latest -g
WORKDIR /bramsplanter/frontend
RUN npm install
# COPY . /amsvd-status
# RUN ["chmod", "+x", "/amsvd-status/wait-for-it.sh"]
# ENV PYTHONPATH "/amsvd-status"

