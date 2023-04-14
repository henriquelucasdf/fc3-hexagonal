FROM python:3.8.15-slim-buster

COPY requirements.txt .

RUN apt update -y\
    && apt-get install git -y\
    && pip install -r requirements.txt

# Creates "python" user
RUN useradd -ms /bin/bash python

USER python

WORKDIR /home/python/app

ENV PIP_ENV_VENV_IN_PROJECT=True

ENV PYTHONPATH="$PYTHONPATH:/home/python/app" 

CMD [ "tail", "-f", "/dev/null" ]