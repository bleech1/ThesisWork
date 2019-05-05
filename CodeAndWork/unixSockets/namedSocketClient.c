/*
 * namedSocketClient.c
 */

// This program connects to a UNIX domain socket

#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/un.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
    char *socketPath = "named";
    
    int sockFd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (sockFd < 0)
    {
        perror("socket");
        exit(1);
    }

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, socketPath, sizeof(addr.sun_path)-1);

    int retVal = connect(sockFd, (struct sockaddr*) &addr, sizeof(addr));
    if (retVal < 0)
    {
        perror("connect");
        exit(1);
    }

    int bytesRead = 10;
    char buf[100];
    int bytesRecv;
    while (bytesRead > 0)
    {
        memset(buf, 0, 100);
        bytesRead = read(0, buf, 100);
        if (bytesRead < 0)
        {
            perror("read");
            exit(1);
        }
        retVal = send(sockFd, buf, bytesRead, 0);
        if (retVal < 0)
        {
            perror("send");
            exit(1);
        }
        bytesRecv = recv(sockFd, buf, 100, 0);
        if (bytesRecv < 0)
        {
            perror("recv");
            exit(1);
        }
        printf("received: %s\n", buf);
        
    }

}
