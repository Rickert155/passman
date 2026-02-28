FROM ubuntu

RUN apt update && apt install fish vim -y
RUN /usr/bin/fish -c "set -U fish_greeting"
RUN echo "fish" >> /root/.bashrc

WORKDIR /root/passman
COPY passman.py .
