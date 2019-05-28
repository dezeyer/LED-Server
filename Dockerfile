FROM python:3.7.2-stretch

#Code Remote Plugin is not compatible with alpine :(
#RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
#RUN apk add --update --no-cache ca-certificates gcc g++ curl openblas-dev@community
#RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN pip3 install --upgrade pip
# Python Development Tools
RUN pip3 install --no-cache-dir --upgrade ptvsd 
RUN pip3 install --no-cache-dir pylint 
RUN pip3 install --no-cache-dir mypy 

# Just to get a message that this is not a raspberry pi
RUN pip3 install --no-cache-dir RPi.GPIO 

# Pulseaudio for the audiorecorder development
RUN pip3 install git+https://github.com/GeorgeFilipkin/pulsemixer.git
ENV UNAME pacat

RUN DEBIAN_FRONTEND=noninteractive apt-get update --yes \
 && DEBIAN_FRONTEND=noninteractive apt-get upgrade --yes \
 &&  DEBIAN_FRONTEND=noninteractive apt-get install --yes pulseaudio \
 && DEBIAN_FRONTEND=noninteractive apt-get install --yes alsa-utils
RUN adduser root audio
RUN adduser root pulse-access
 
 RUN echo "load-module module-native-protocol-tcp port=34567 auth-anonymous=1" >> /etc/pulse/system.pa
#Not sure if this is needed for audiorecorder
#RUN pip3 install --no-cache-dir scipy
#defenetly needed for audio recorder, also the musicEffect
RUN pip3 install --no-cache-dir numpy
# pyaudio to record audio
RUN DEBIAN_FRONTEND=noninteractive apt-get install --yes portaudio19-dev
RUN pip3 install --no-cache-dir pyaudio
RUN pip3 install --no-cache-dir matplotlib



# import my ssh key to be able to use github
RUN mkdir ~/.ssh && \ 
    ln -s /run/secrets/host_ssh_key ~/.ssh/id_rsa && \ 
    ssh-keyscan github.com >> ~/.ssh/known_hosts

#CMD ["pacat", "-vvvv", "/dev/urandom"]
CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"

