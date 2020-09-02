FROM ubuntu:18.04

RUN apt -y update && apt -y upgrade && apt -y install build-essential python3-pip python-dev

COPY flag.txt /app/flag
COPY server.py /app/

EXPOSE 2468
WORKDIR /app

RUN pip3 install secretpy

ENTRYPOINT ["python3"]
CMD ["server.py"]
