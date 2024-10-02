FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip

RUN apt-get install -y adb fastboot

COPY ./app/requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

COPY ./app /usr/local/app/
COPY ./downloads /usr/local/downloads/

WORKDIR /usr/local/app/
