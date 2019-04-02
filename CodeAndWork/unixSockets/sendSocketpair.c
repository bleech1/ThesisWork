/*
 * sendSocketpair.c
 */

// This program creates a socketpair, then from the child, sends the fd
// to another program

#include <sys/socket.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/un.h>

#define SOCKET_NAME "socket_name"

int SendFd(int fd);

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

        // Send the fd to another process via named socket
        retVal = SendFd(sockets[1]);
        if (retVal < 0)
        {
            perror("sendfd");
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

int SendFd(int fd)
{
    int sockFd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (sockFd < 0)
    {
        perror("socket");
        exit(1);
    }

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, SOCKET_NAME, sizeof(addr.sun_path)-1);
    unlink(SOCKET_NAME);

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

    int clientFd = accept(sockFd, NULL, NULL);
    if (clientFd < 0)
    {
        perror("accept");
        exit(1);
    }

    // Send the socktpair fd through the socket
    // sendmsg code from: https://stackoverflow.com/questions/28003921/sending-file-descriptor-by-linux-socket
    struct msghdr msg = { 0 };
    char buf[CMSG_SPACE(sizeof(fd))];
    memset(buf, '\0', sizeof(buf));

    // On Mac OS X, the struct iovec is needed, even if it points to minimal data
    struct iovec io = { .iov_base = "", .iov_len = 1 };

    msg.msg_iov = &io;
    msg.msg_iovlen = 1;
    msg.msg_control = buf;
    msg.msg_controllen = sizeof(buf);

    struct cmsghdr * cmsg = CMSG_FIRSTHDR(&msg);
    cmsg->cmsg_level = SOL_SOCKET;
    cmsg->cmsg_type = SCM_RIGHTS;
    cmsg->cmsg_len = CMSG_LEN(sizeof(fd));

    memmove(CMSG_DATA(cmsg), &fd, sizeof(fd));

    msg.msg_controllen = CMSG_SPACE(sizeof(fd));
    int sendResult = sendmsg(clientFd, &msg, 0);
    if (sendResult < 0)
    {
        perror("sendmsg");
        exit(1);
    }
    retVal = close(clientFd);
    if (retVal < 0)
    {
        perror("close");
        exit(1);
    }
    retVal = close(sockFd);
    if (retVal < 0)
    {
        perror("close");
        exit(1);
    }
    return 0;
}
