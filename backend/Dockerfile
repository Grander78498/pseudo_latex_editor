FROM python:3.12

ADD requirements.txt /requirements.txt

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

ENV DB_HOST=pgdb
ENV DB_PORT=5432
ENV DB_NAME=db_formula
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres

RUN mkdir -p /app/backend
WORKDIR /app/backend
ADD . /app/backend/
RUN chmod +x /app/backend/entrypoint.sh

ENTRYPOINT [ "/app/backend/entrypoint.sh" ]
