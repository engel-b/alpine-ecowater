FROM python:3.8.12-alpine3.14

COPY ca.crt .
COPY crontab .
COPY ecowater.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

RUN crontab crontab

CMD ["crond", "-f"]

