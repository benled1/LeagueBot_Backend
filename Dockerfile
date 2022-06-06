FROM python:3.9-bullseye
ENV PYTHONUNBUFFERED=1
ENV RIOT_KEY=RGAPI-c8eea596-a3cb-4b54-be61-731a9bc5ba4c
WORKDIR /workspace
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

