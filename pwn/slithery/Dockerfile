FROM ubuntu:18.04

RUN apt -y update && apt -y upgrade && apt -y install build-essential python3-pip python-dev

COPY flag.txt /app/flag
COPY *.py /app/

EXPOSE 2354
WORKDIR /app

RUN pip3 install numpy

ENTRYPOINT ["python3"]
CMD ["runner.py"]
