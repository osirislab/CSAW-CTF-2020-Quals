FROM ubuntu:18.04

RUN apt -y update && apt -y upgrade && apt -y install python3-pip

COPY flag.txt /app/flag
COPY encrypt.py /app/encrypt.py

EXPOSE 2468
WORKDIR /app

RUN pip3 install pycrypto

ENTRYPOINT ["python3"]
CMD ["encrypt.py"]
