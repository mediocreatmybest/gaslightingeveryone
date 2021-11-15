FROM nvidia/cuda:11.4.1-cudnn8-runtime-ubuntu18.04

# Setup the basics first
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y bash && \
    apt-get install -y git-core && \
    apt-get install -y wget && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get install -y libglib2.0-0

# Install miniconda
RUN MINICONDA="Miniconda3-latest-Linux-x86_64.sh" && \
    wget --quiet https://repo.anaconda.com/miniconda/$MINICONDA && \
    bash $MINICONDA -b -p /miniconda && \
    rm -f $MINICONDA
ENV PATH /miniconda/bin:$PATH


# Install Python and Py/Additionals


RUN conda --version
RUN pip install --upgrade pip 
RUN pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install opencv-python scipy tqdm yapf lmdb pyyaml tb-nightly wheel
RUN pip install basicsr facexlib realesrgan


WORKDIR /
RUN git clone https://github.com/TencentARC/GFPGAN GFPGAN
WORKDIR /GFPGAN
RUN wget https://github.com/TencentARC/GFPGAN/releases/download/v0.2.0/GFPGANCleanv1-NoCE-C2.pth -P experiments/pretrained_models
RUN python setup.py develop
RUN python inference_gfpgan.py --upscale 2 --test_path inputs/whole_imgs/ --save_root result

ENV NVIDIA_DRIVER_CAPABILITIES all
ENV DEBIAN_FRONTEND teletype
