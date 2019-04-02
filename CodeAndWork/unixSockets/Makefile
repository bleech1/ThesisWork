.PHONY: all
all: socketpair anonSocket namedSocket namedSocketClient sendSocketpair receiveSocketpair

CFLAGS=-g -Wall -pedantic

socketpair: socketpair.c
	gcc $(CFLAGS) -o $@ $^

anonSocket: anonSocket.c
	gcc $(CFLAGS) -o $@ $^

namedSocket: namedSocket.c
	gcc $(CFLAGS) -o $@ $^ 

namedSocketClient: namedSocketClient.c
	gcc $(CFLAGS) -o $@ $^

sendSocketpair: sendSocketpair.c
	gcc $(CFLAGS) -o $@ $^

receiveSocketpair: receiveSocketpair.c
	gcc $(CFLAGS) -o $@ $^

.PHONY: clean
clean:
	rm socketpair anonSocket namedSocket namedSocketClient sendSocketpair receiveSocketpair