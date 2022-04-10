FROM python:3.9-bullseye
ENV PYTHONUNBUFFERED=1
ENV RIOT_KEY=RGAPI-ead7e96f-8a56-405d-a0e8-143676092505
WORKDIR /workspace
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
