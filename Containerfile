FROM ubuntu

RUN apt update && apt install fish vim -y
RUN /usr/bin/fish -c "set -U fish_greeting"
RUN echo "fish" >> /root/.bashrc
RUN echo "alias passman='python3 /root/passman/__main__.py'" >> /root/.config/fish/config.fish

WORKDIR /root/passman
COPY passman/__main__.py .
