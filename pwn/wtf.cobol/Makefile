all: clean wtf

.PHONY: wtf
wtf:
	cobc -free -Wall -Wcolumn-overflow -g -x -o wtf wtf.cobol

socat: wtf
	socat -T60 TCP-LISTEN:5000,reuseaddr,fork EXEC:./wtf,stderr

clean:
	rm -f *.c *.h *.i wtf
