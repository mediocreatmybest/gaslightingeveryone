FROM python:2.7-slim	
	
# install deps
RUN apt-get update && apt-get -y install \
    git-core build-essential software-properties-common gcc libssl-dev hashcat wget curl

RUN apt-get clean && rm -rf /var/lib/apt/lists/*	
COPY requirements.txt /requirements.txt

RUN python2.7 -m pip install --upgrade pip && \	
	python2.7 -m pip install --no-cache-dir -r /requirements.txt

WORKDIR /	
RUN git clone https://github.com/gurnec/btcrecover btcrecover
WORKDIR /btcrecover

ENV NVIDIA_DRIVER_CAPABILITIES all
