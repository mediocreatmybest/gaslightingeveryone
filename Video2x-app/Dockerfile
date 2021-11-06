FROM ubuntu:19.10

RUN sed -i 's/archive.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list

# run installation
RUN apt-get update \
    && apt-get install -y git-core \
    && git clone --recurse-submodules --progress https://github.com/k4yt3x/video2x.git /tmp/video2x/video2x \
    && bash -e /tmp/video2x/video2x/src/video2x_setup_ubuntu.sh /

ENTRYPOINT ["/bin/bash"]

ENV NVIDIA_DRIVER_CAPABILITIES all
ENV DEBIAN_FRONTEND teletype