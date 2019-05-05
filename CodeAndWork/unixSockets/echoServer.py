# echo server UNIX domain sockets

import threading
import socket

server_address = "named"
BUF_SIZE = 1024

def main():
    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(10)

    while True:
        # Wait for a connection
        connection, client_address = sock.accept()
        recvThread = threading.Thread(target = EchoBack, args = [connection])
        recvThread.daemon = True
        recvThread.start()

def EchoBack(connection):
    while 1:
        data = connection.recv(BUF_SIZE)
        if len(data) == 0:
            break
        print("received: " + data.decode("utf-8"))
        connection.send(data)

    connection.close()

if __name__ == "__main__":
    main()