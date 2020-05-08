FROM alpine:latest

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip
RUN apk add  --no-cache ffmpeg

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade youtube-dl

RUN adduser -DH -u 1000 qmk 1000

COPY . .

CMD [ "python3", "./run.py" ]