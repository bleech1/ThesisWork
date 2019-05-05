.PHONY: all
all: getNamedMessages namedServer connectTcp connectUdp udpServer

CFLAGS=-g -Wall -pedantic

getNamedMessages: getNamedMessages.c
	gcc $(CFLAGS) -o $@ $<

namedServer: namedServer.c
	gcc $(CFLAGS) -o $@ $<

connectTcp: connectTcp.c
	gcc $(CFLAGS) -o $@ $<

connectUdp: connectUdp.c
	gcc $(CFLAGS) -o $@ $<

udpServer: udpServer.c
	gcc $(CFLAGS) -o $@ $<

.PHONY: code1
code1: getNamedMessages
	./getNamedMessages "/Users/Bleecher/Library/Application Support/Code/1.33.1-main.sock"

.PHONY: code2
code2: getNamedMessages
	./getNamedMessages  /var/folders/th/3_4wg0x53w7_01g6m_2fd5rr0000gn/T/vscode-ipc-09804ca6-7c84-453d-a081-1ee5b80d6bed.sock

.PHONY: code3
code3: getNamedMessages
	./getNamedMessages /var/folders/th/3_4wg0x53w7_01g6m_2fd5rr0000gn/T/vscode-git-askpass-612855994448e69a1d9c13a0ad0f64901b2

.PHONY: code9
code9: getNamedMessages 
	./getNamedMessages "/Users/Bleecher/Library/Application Support/Code/1.33.1-shared.sock"

.PHONY: code4
code4: namedServer
	./namedServer "/Users/Bleecher/Library/Application Support/Code/1.33.1-shared.sock"

.PHONY: code5
code5: namedServer
	./namedServer "/Users/Bleecher/Library/Application Support/Code/1.33.1-main.sock"

.PHONY: tcpCode
tcpCode: connectTcp
	./connectTcp 26334

.PHONY: tcpCode2
tcpCode2: connectTcp
	./connectTcp 59869
 
.PHONY: clean
clean:
	rm -r connectTcp connectTcp.dSYM
	rm -r connectUdp connectUdp.dSYM
	rm -r getNamedMessages getNamedMessages.dSYM
	rm -r namedServer namedServer.dSYM
	rm -r udpServer udpServer.dSYM
	rm -r unixConnectDatagram unixConnectDatagram.dSYM
