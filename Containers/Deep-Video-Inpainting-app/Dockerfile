FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04

# Setup the basics first
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y apt-utils \
    && apt-get install -y bash ffmpeg \
    && apt-get install -y git-core \
    && apt-get install -y wget \
    && apt-get install -y youtube-dl \
    && apt-get install -y unzip 

# Add Additional Software and Cleanup
RUN apt update && \
    apt install --no-install-recommends -y software-properties-common \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Install miniconda
	RUN wget && \
	MINICONDA="Miniconda3-latest-Linux-x86_64.sh" && \
	wget --quiet https://repo.anaconda.com/miniconda/$MINICONDA && \
	bash $MINICONDA -b -p /miniconda && \
	rm -f $MINICONDA
	ENV PATH /miniconda/bin:$PATH


# Install Python and Py/Additionals


    RUN conda --version
    RUN conda install -c anaconda python=3.7 -y
    RUN conda install pytorch=1.4 torchvision cudatoolkit=10.0 -c pytorch -y

# Set / as Working DIR
WORKDIR /

# GIT Clone Required Programs / Files
RUN git clone https://github.com/mcahny/Deep-Video-Inpainting deep_video_inpainting


#move into pre-trained model working dir
WORKDIR /deep_video_inpainting/results/vinet_agg_rec/


# Project Requirements / add pre-trained models / Install Scripts
RUN python3.7 -m pip install --upgrade pip && \	
	python3.7 -m pip install --no-cache-dir gdown
RUN gdown https://drive.google.com/uc?id=1KAi9oQVBaJU9ytr7dYr2WwEcO5NLiJvo 

WORKDIR /deep_video_inpainting/
RUN bash install.sh
WORKDIR /

ENV NVIDIA_DRIVER_CAPABILITIES all
ENV DEBIAN_FRONTEND teletype
