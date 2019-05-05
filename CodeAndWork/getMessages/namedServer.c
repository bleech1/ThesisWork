/*
 * namedServer.c
 */

// This program makes a normal UNIX domain socket without a name

#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/un.h>
#include <string.h>
#include <unistd.h>

#define MAX_BYTES_READ 4096

void Usage();
void PrintHex(char *str, int len);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        Usage();
        exit(1);
    }
    char *socketPath = argv[1];
    
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
    unlink(socketPath);

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

    int readResult = 10;
    char buf[MAX_BYTES_READ];
    int clientFd = accept(sockFd, NULL, NULL);
    if (clientFd < 0)
    {
        perror("accept");
        exit(1);
    }
    while (1)
    {
        memset(buf, 0, MAX_BYTES_READ);
        readResult = read(clientFd, buf, MAX_BYTES_READ);
        if (readResult < 0)
        {
            perror("read");
            exit(1);
        }
        if (readResult == 0)
        {
            continue;
        }
        printf("num recieved: %d\n", readResult);
        PrintHex(buf, readResult);
    }
}

void Usage()
{
    printf("Usage: namedServer sockName\n");
}

void PrintHex(char *str, int len)
{
    char *temp = str;
    printf("length: %d\n", len);
    for (int i = 0; i < len; i ++)
    {
        printf("%02x ", (*(temp + i) & 0xff));
    }
    printf("\n");
}
