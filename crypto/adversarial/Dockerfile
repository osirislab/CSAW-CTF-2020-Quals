FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y python python-pip

RUN pip install pycrypto gunicorn

COPY . /chal
WORKDIR /chal

EXPOSE 5000

CMD ["gunicorn", "-w", "40", "-b", "0.0.0.0:5000", "server:server"]
