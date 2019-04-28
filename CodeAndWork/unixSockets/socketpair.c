/*
 * socketpair.c
 */

// This program uses socketpair to see how these sockets appear in the
// output of lsof

#include <sys/socket.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
    int sockets[2];

    // make the two sockets
    int retVal = socketpair(AF_LOCAL, SOCK_DGRAM, 0, sockets);
    if (retVal < 0)
    {
        perror("socketpair");
        exit(1);
    }

    // fork
    int childPid = fork();
    if (childPid < 0)
    {
        perror("fork"); // fork error
        exit(1);
    }
    else if (childPid == 0)
    {
        // in the child, will close 0th socket fd
        retVal = close(sockets[0]);
        if (retVal < 0)
        {
            perror("close");
            exit(1);
        }
        // read from stdin and write to socket
        char buf[100];
        while (1)
        {
            retVal = read(0, buf, 100);
            if (retVal < 0)
            {
                perror("read");
                exit(1);
            }
            retVal = send(sockets[1], buf, retVal, 0);
            if (retVal < 0)
            {
                perror("send");
                exit(1);
            }
        }
    }
    else
    {
        // in the parent, will close 1st socket fd
        retVal = close(sockets[1]);
        if (retVal < 0)
        {
            perror("close");
            exit(1);
        }
        // read from socket and print out
        char buf[100];
        while (1)
        {
            retVal = recv(sockets[0], buf, 100, 0);
            if (retVal < 0)
            {
                perror("recv");
                exit(1);
            }
            printf("Received: %s", buf);
        }
    }
    
}
