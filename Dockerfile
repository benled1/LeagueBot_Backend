FROM python:3.9-bullseye
ENV PYTHONUNBUFFERED=1
WORKDIR /workspace
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

