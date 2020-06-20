FROM alpine:latest

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip
RUN apk add  --no-cache ffmpeg
RUN apk add  --no-cache python

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ARG user_id=1000
ARG group_id=user_id
RUN adduser -DH -u ${user_id} qmk ${user_id}

COPY . .

CMD [ "python3", "./run.py" ]