FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y python python-pip

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . /chal
WORKDIR /chal

EXPOSE 5000

CMD ["gunicorn", "-w", "40", "-b", "0.0.0.0:5000", "server:server"]
