FROM python:3.8-slim	
	
# install deps
RUN apt-get update && apt-get -y install \
git-core
	
COPY requirements.txt /requirements.txt

RUN python3.8 -m pip install --upgrade pip && \	
	python3.8 -m pip install --no-cache-dir -r /requirements.txt

WORKDIR /	
RUN git clone https://github.com/ryepdx/pyethrecover recover-wallet
WORKDIR /recover-wallet

ENTRYPOINT ["/bin/bash"]
	
ENV NVIDIA_DRIVER_CAPABILITIES all