FROM alpine:3.7

ENV FLASK_APP=main.py

WORKDIR /srv/apps/dynamic-mock-harvest-source

COPY main.py main.py
COPY requirements.txt requirements.txt
COPY test.tmp.xml test.tmp.xml

RUN apk add --no-cache python3 curl

RUN curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    pip install -r requirements.txt

EXPOSE 8001

CMD python3 main.py
