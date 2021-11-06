#FROM nvidia/cuda:11.3.0-cudnn8-runtime-ubi7
#FROM nvidia/cuda:11.4.2-devel-ubuntu20.04
FROM nvidia/cuda:11.4.1-base-ubuntu18.04
# Setup the basics first
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y apt-utils \
    && apt-get install -y bash ffmpeg \
    && apt-get install -y git-core \
    && apt-get install -y wget \
    && apt-get install -y youtube-dl \
    && apt-get install -y unzip 

# Add Additional Python
RUN apt update && \
    apt install --no-install-recommends -y build-essential g++-8 software-properties-common && \
    apt install --no-install-recommends -y python3.8 python3-pip python3-setuptools python3-distutils && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt

RUN python3.8 -m pip install --upgrade pip && \
    python3.8 -m pip install --no-cache-dir -r /requirements.txt

#Copy folder over if needed
#COPY ./src-example /src-example
#CMD ['python3', '/src/app.py']


#INSTALL RIFE ARXIV2020 - See https://github.com/hzwer/arXiv2020-RIFE

#WORKDIR /rife

#RUN git clone https://github.com/hzwer/arXiv2020-RIFE
#RUN cp arXiv2020-RIFE/docker/inference_img /usr/local/bin/inference_img
#RUN chmod +x /usr/local/bin/inference_img
#RUN cp arXiv2020-RIFE/docker/inference_video /usr/local/bin/inference_video
#RUN chmod +x /usr/local/bin/inference_video

# add pre-trained models
#RUN gdown https://drive.google.com/uc?id=1APIzVeI-4ZZCEuIRE1m6WYfSCaOsi_7_ && \
#    unzip RIFE_trained_model_v3.6.zip

#COPY train_log /rife/train_log

WORKDIR /
RUN git clone https://github.com/braindotai/Watermark-Removal-Pytorch watermark-removal

# run installation for VIDEO2X
#ENV CMAKE_CXX_COMPILER="g++"
#RUN apt-get update \
#    && git clone --recurse-submodules --progress https://github.com/k4yt3x/video2x.git /tmp/video2x/video2x \
#    && bash -e /tmp/video2x/video2x/src/video2x_setup_ubuntu.sh /


#ENTRYPOINT ["/bin/bash"]
#ENTRYPOINT [ "/bin/bash", "-l", "-c" ]
ENV NVIDIA_DRIVER_CAPABILITIES all
ENV DEBIAN_FRONTEND teletype

#Move into QNAP Build
#ENV PATH=$PATH:/usr/local/nividia/bin 
#ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib:/usr/local/nvidia/lib:/usr/local/nvidia/lib64

