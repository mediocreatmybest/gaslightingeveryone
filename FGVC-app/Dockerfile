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
    apt install --no-install-recommends -y software-properties-common && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Install miniconda
	RUN MINICONDA="Miniconda3-latest-Linux-x86_64.sh" && \
	wget --quiet https://repo.anaconda.com/miniconda/$MINICONDA && \
	bash $MINICONDA -b -p /miniconda && \
	rm -f $MINICONDA
	ENV PATH /miniconda/bin:$PATH


# Install Python and Py/Additionals


    RUN conda --version
    RUN conda install -c anaconda python=3.8 -y
    RUN conda install pytorch=1.6.0 torchvision=0.7.0 cudatoolkit=10.1 -c pytorch -y
    RUN conda install matplotlib scipy imageio scikit-image
    RUN pip install --upgrade pip 
    RUN pip install opencv-python opencv-contrib-python

# Set / as Working DIR
WORKDIR /

# GIT Clone Required Programs / Files
RUN git clone https://github.com/vt-vl-lab/FGVC FGVC

# Project Requirements / add pre-trained models / Install Scripts

WORKDIR /FGVC/

RUN wget --no-check-certificate https://filebox.ece.vt.edu/~chengao/FGVC/data.zip \
    && unzip data.zip \
    && rm data.zip \
    && wget --no-check-certificate https://filebox.ece.vt.edu/~chengao/FGVC/weight.zip \
    && unzip weight.zip \
    && rm weight.zip



ENV NVIDIA_DRIVER_CAPABILITIES all
ENV DEBIAN_FRONTEND teletype
