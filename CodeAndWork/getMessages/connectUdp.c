#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <string.h> 
#include <sys/types.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <netinet/in.h> 
  
#define MAX_BYTES_READ 4096

void Usage();
void PrintHex(char *str, int len);
  
// Driver code 
int main(int argc, char *argv[])
{ 
    if (argc != 2)
    {
        Usage();
        exit(1);
    }

    char *port = argv[1];
    // lengths of 50 and 68
    //char *message = "\x45\x7f\x01\x10\x00\x01\x00\x00\x00\x00\x00\x00\x20\x41\x42\x41\x43\x46\x50\x46\x50\x45\x4e\x46\x44\x45\x43\x46\x43\x45\x50\x46\x48\x44\x44\x45\x46\x46\x50\x46\x50\x41\x43\x41\x42\x00\x00\x20\x00\x01";
    //char *message = "\x45\x81\x29\x10\x00\x01\x00\x00\x00\x00\x00\x01\x20\x45\x43\x46\x43\x45\x46\x45\x4f\x45\x45\x45\x42\x45\x4f\x46\x44\x43\x4e\x45\x4e\x45\x43\x46\x41\x43\x41\x43\x41\x43\x41\x41\x41\x00\x00\x20\x00\x01\xc0\x0c\x00\x20\x00\x01\x00\x00\x03\x84\x00\x06\x60\x00\x8c\xe9\xaa\x7e";
    char *message = "\x00\x00\x00\x00\x00\x11\x00\x01\x00\x00\x00\x00\x08\x5f\x61\x69\x72\x70\x6f\x72\x74\x04\x5f\x74\x63\x70\x05\x6c\x6f\x63\x61\x6c\x00\x00\x0c\x00\x01\x08\x5f\x61\x69\x72\x70\x6c\x61\x79\xc0\x15\x00\x0c\x00\x01\x05\x5f\x72\x61\x6f\x70\xc0\x15\x00\x0c\x00\x01\x07\x5f\x69\x70\x70\x75\x73\x62\xc0\x15\x00\x0c\x00\x01\x06\x5f\x75\x73\x63\x61\x6e\xc0\x15\x00\x0c\x00\x01\x08\x5f\x70\x72\x69\x6e\x74\x65\x72\xc0\x15\x00\x0c\x00\x01\x04\x5f\x69\x70\x70\xc0\x15\x00\x0c\x00\x01\x07\x5f\x75\x73\x63\x61\x6e\x73\xc0\x15\x00\x0c\x00\x01\x04\x5f\x70\x74\x70\xc0\x15\x00\x0c\x00\x01\x0f\x5f\x70\x64\x6c\x2d\x64\x61\x74\x61\x73\x74\x72\x65\x61\x6d\xc0\x15\x00\x0c\x00\x01\x08\x5f\x73\x63\x61\x6e\x6e\x65\x72\xc0\x15\x00\x0c\x00\x01\x05\x5f\x69\x70\x70\x73\xc0\x15\x00\x0c\x00\x01\x07\x5f\x72\x64\x6c\x69\x6e\x6b\xc0\x15\x00\x0c\x00\x01\x0f\x5f\x63\x6f\x6d\x70\x61\x6e\x69\x6f\x6e\x2d\x6c\x69\x6e\x6b\xc0\x15\x00\x0c\x00\x01\x0d\x5f\x61\x70\x70\x6c\x65\x2d\x6d\x6f\x62\x64\x65\x76\xc0\x15\x00\x0c\x00\x01\x08\x38\x62\x61\x65\x30\x37\x63\x30\x04\x5f\x73\x75\x62\x0e\x5f\x61\x70\x70\x6c\x65\x2d\x6d\x6f\x62\x64\x65\x76\x32\xc0\x15\x00\x0c\x00\x01\x0f\x5f\x61\x70\x70\x6c\x65\x2d\x70\x61\x69\x72\x61\x62\x6c\x65\xc0\x15\x00\x0c\x00\x01\xc0\xcd\x00\x0c\x00\x01\x00\x00\x0d\x9e\x00\x1a\x17\x42\x72\x65\x6e\x64\x61\x6e\xe2\x80\x99\x73\x20\x4d\x61\x63\x42\x6f\x6f\x6b\x20\x50\x72\x6f\xc0\xcd";

    int sockfd; 
    char buffer[MAX_BYTES_READ]; 
    struct sockaddr_in     servaddr; 
  
    // Creating socket file descriptor 
    if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) { 
        perror("socket"); 
        exit(1); 
    } 
  
    memset(&servaddr, 0, sizeof(servaddr)); 
      
    // Filling server information 
    servaddr.sin_family = AF_INET; 
    servaddr.sin_port = htons(atoi(port)); 
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1"); 
      
    int n, len; 
      
    while (1)
    {
        sendto(sockfd, (const char *)message, 342, 0, (const struct sockaddr *) &servaddr,  
                sizeof(servaddr)); 
        printf("Hello message sent.\n"); 
            
        n = recvfrom(sockfd, (char *)buffer, MAX_BYTES_READ,  
                    0, (struct sockaddr *) NULL, 0); 
        buffer[n] = '\0'; 
        printf("Server : %s\n", buffer); 
        PrintHex(buffer, n);
    }
  
    close(sockfd); 
    return 0; 
} 

void Usage()
{
    printf("Usage: udpServer port\n");
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
