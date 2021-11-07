FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04

# Setup the basics first
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update \
    && apt-get install -y apt-utils \
    && apt-get install -y bash ffmpeg \
    && apt-get install -y git-core \
    && apt-get install -y wget \
    && apt-get install -y youtube-dl \
    && apt-get install -y unzip 

# Add Additional Software and Cleanup
RUN apt update && \
    apt install --no-install-recommends -y software-properties-common
    apt clean && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 
RUN conda --version
RUN conda install -c anaconda python=3.7 -y
RUN conda install pytorch=1.4 torchvision cudatoolkit=10.0 -c pytorch -y

WORKDIR /

RUN git clone https://github.com/mcahny/Deep-Video-Inpainting deep_video_inpainting


#move into pre-trained model working dir
WORKDIR /deep_video_inpainting/results/vinet_agg_rec/



# add pre-trained models
RUN python3.7 -m pip install --upgrade pip && \	
	python3.7 -m pip install --no-cache-dir gdown
RUN gdown https://drive.google.com/uc?id=1KAi9oQVBaJU9ytr7dYr2WwEcO5NLiJvo 

WORKDIR /deep_video_inpainting/
RUN bash install.sh
WORKDIR /

ENV NVIDIA_DRIVER_CAPABILITIES all
ENV DEBIAN_FRONTEND teletype
