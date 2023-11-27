FROM alpine:3.18.4
LABEL name="constellation"
LABEL description="A WebSocket server for the Darkmatter website stars wallpaper."
LABEL maintainer="Anthony Waldsmith <awaldsmith@protonmail.com>"

# Install dependencies
RUN apk add --update py3-pip python3

COPY requirements.txt /tmp/

RUN pip3 install -r /tmp/requirements.txt \
	&& rm /tmp/requirements.txt

EXPOSE 8080/tcp

CMD ["python3", "./src/"]
