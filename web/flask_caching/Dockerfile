FROM python:3.8-alpine

WORKDIR /opt/app
COPY requirements.txt requirements.txt

RUN apk add --update --no-cache curl redis supervisor \
  && pip3 install -r requirements.txt \
  && adduser -DH www

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY . .

RUN mv flag.txt /flag.txt \
  && chmod 444 /flag.txt \
  && chmod 444 ./app.py

CMD ["supervisord", "-l", "/dev/null"]


