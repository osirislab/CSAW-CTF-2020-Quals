FROM ubuntu:18.04
MAINTAINER tnek
RUN apt-get update && apt-get install -y socat

RUN useradd -ms /bin/sh elemental
WORKDIR /home/elemental

COPY ./elemental ./
COPY ./flag.txt ./

RUN chown -R root:elemental /home/elemental && \
     chmod 750 /home/elemental && \
     chmod 550 /home/elemental/elemental && \
     chown root:elemental /home/elemental/flag.txt && \
     chmod 440 /home/elemental/flag.txt

EXPOSE 8000

CMD ["socat", "-T60", "TCP-LISTEN:8000,reuseaddr,fork,su=elemental","EXEC:/home/elemental/elemental"]
