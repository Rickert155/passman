FROM alpine 

RUN apk add vim fish python3

RUN /usr/bin/fish -c "set -U fish_greeting"
RUN echo "alias passman='python3 /root/passman/__main__.py'" >> /root/.config/fish/config.fish

WORKDIR /root/passman
COPY passman/__main__.py .
WORKDIR /root/

CMD ["fish"]
