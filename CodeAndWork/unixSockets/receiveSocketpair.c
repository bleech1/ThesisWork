/*
 * receiveSocketpair.c
 */

// This program connects to a socket, recieves a descriptor representing a UNIX
// socket made with socketpair, and sends data from stdin

#include <sys/socket.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/un.h>

#define SOCKET_NAME "socket_name"

int main(int argc, char *argv[])
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

    int retVal = connect(sockFd, (struct sockaddr*) &addr, sizeof(addr));
    if (retVal < 0)
    {
        perror("connect");
        exit(1);
    }

    // use recvmsg to get the socketpair descriptor
    // recvmsg code from: https://stackoverflow.com/questions/28003921/sending-file-descriptor-by-linux-socket
    struct msghdr msg = {0};

    /* On Mac OS X, the struct iovec is needed, even if it points to minimal data */
    char m_buffer[1];
    struct iovec io = { .iov_base = m_buffer, .iov_len = sizeof(m_buffer) };
    msg.msg_iov = &io;
    msg.msg_iovlen = 1;

    char c_buffer[256];
    msg.msg_control = c_buffer;
    msg.msg_controllen = sizeof(c_buffer);

    if (recvmsg(sockFd, &msg, 0) < 0)
    {
        perror("recvmsg");
        exit(1);
    }

    struct cmsghdr *cmsg = CMSG_FIRSTHDR(&msg);

    int pairFd;
    memmove(&pairFd, CMSG_DATA(cmsg), sizeof(pairFd));

    retVal = close(sockFd);
    if (retVal < 0)
    {
        perror("close");
        exit(1);
    }

    // read from stdin and send to socketpair socket
    int bytesRead = 10;
    char buf[100];
    while (bytesRead > 0)
    {
        bytesRead = read(0, buf, 100);
        if (bytesRead < 0)
        {
            perror("read");
            exit(1);
        }
        retVal = send(pairFd, buf, bytesRead, 0);
        if (retVal < 0)
        {
            perror("send");
            exit(1);
        }
    }
}
