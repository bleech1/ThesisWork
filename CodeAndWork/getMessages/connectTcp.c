/*
 * connectTcp.c
 */

#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>

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

    char *port = argv[1];

    int sockFd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockFd < 0)
    {
        perror("socket");
        exit(1);
    }

    struct addrinfo hints;
    struct addrinfo *res;
    int rc;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    if((rc = getaddrinfo("localhost", port, &hints, &res)) != 0)
    {
        printf("getaddrinfo failed: %s\n", gai_strerror(rc));
        exit(1);
    }

    // Connect to server
    if(connect(sockFd, res->ai_addr, res->ai_addrlen) < 0)
    {
        perror("connect");
        exit(1);
    }

    int bytesRead = 10;
    char buf[MAX_BYTES_READ];
    char message[MAX_BYTES_READ];
    while (bytesRead > 0)
    {
        char *page = "/bleech1/ThesisWork";
        char *host = "www.github.com";
        snprintf(message, MAX_BYTES_READ, 
     "GET %s HTTP/1.1\r\n"  // POST or GET, both tested and works. Both HTTP 1.0 HTTP 1.1 works, but sometimes 
     "Host: %s\r\n"     // but sometimes HTTP 1.0 works better in localhost type
     "Content-type: application/x-www-form-urlencoded\r\n"
     "Content-length: %d\r\n\r\n", page, host, 1000);
        send(sockFd, message, strlen(message), 0);
        bytesRead = read(sockFd, buf, MAX_BYTES_READ);
        if (bytesRead < 0)
        {
            perror("read");
            exit(1);
        }
        printf("mesage: %s\n", buf);
        PrintHex(buf, bytesRead);
    }

}

void Usage()
{
    printf("connectTcp portNum\n");
}

void PrintHex(char *str, int len)
{
    char *temp = str;
    for (int i = 0; i < len; i ++)
    {
        printf("%02x ", (*(temp + i) & 0xff));
    }
    printf("\n");
}
