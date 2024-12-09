FROM python:3.12

ADD requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN mkdir -p /app/backend
WORKDIR /app/backend
ADD . /app/backend/

ENTRYPOINT [ "/app/backend/entrypoint.sh" ]