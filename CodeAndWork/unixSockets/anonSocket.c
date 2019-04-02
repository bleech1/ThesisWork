/*
 * anonSocket.c
 */

// This program makes a normal UNIX domain socket without a name

#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/un.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char *socketPath = "\x0hidden";
    
    int sockFd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (sockFd < 0)
    {
        perror("socket");
        exit(1);
    }

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    *addr.sun_path = '\x0';
    strncpy(addr.sun_path+1, socketPath+1, sizeof(addr.sun_path)-2);

    int retVal = bind(sockFd, (struct sockaddr*) &addr, sizeof(addr));
    if (retVal < 0)
    {
        perror("bind");
        exit(1);
    }

    retVal = listen(sockFd, 10);
    if (retVal < 0)
    {
        perror("listen");
        exit(1);
    }

    int readResult;
    char buf[100];
    while (1)
    {
        int clientFd = accept(sockFd, NULL, NULL);
        if (clientFd < 0)
        {
            perror("accept");
            continue;
        }
        readResult = recv(clientFd, buf, sizeof(buf), 0);
        if (readResult < 0)
        {
            perror("read");
            exit(1);
        }
        printf("Received: %s", buf);
    }
}
