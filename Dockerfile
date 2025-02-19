FROM python:3.12.9-alpine3.21

WORKDIR home
COPY ./ ./

RUN pip3 install -r requirements.txt

CMD "/bin/ash"



