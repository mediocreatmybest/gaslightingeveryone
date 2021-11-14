FROM k4yt3x/video2x

# Setup the basics first
ENV DEBIAN_FRONTEND=noninteractive
RUN sed -i 's/archive.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
RUN apt-get update && \
    apt-get install --no-install-recommends -y vim && \
    apt-get install --no-install-recommends -y unzip

RUN curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl && \
    chmod a+rx /usr/local/bin/youtube-dl
    
#Time to call the cleaners and clean up
RUN apt clean && rm -rf /var/lib/apt/lists/*
WORKDIR /video2x/src


ENTRYPOINT 
ENV NVIDIA_DRIVER_CAPABILITIES all
ENV DEBIAN_FRONTEND teletype
