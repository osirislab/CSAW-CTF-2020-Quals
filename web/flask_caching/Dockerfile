FROM python:3.8-alpine

WORKDIR /opt/app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt \
  && adduser -DH flask

COPY . .

RUN mv flag.txt /flag.txt \
  && chmod ugo-w -R /flag.txt .

CMD python3 app.py
