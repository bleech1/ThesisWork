#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <string.h> 
#include <sys/types.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <netinet/in.h> 
  
#define MAX_BYTES_READ 4096

void PrintHex(char *str, int len);
void Usage();
  
// Driver code 
int main(int argc, char *argv[])
{ 
    if (argc != 2)
    {
        Usage();
        exit(1);
    }

    char *port = argv[1];

    int sockfd; 
    char buffer[MAX_BYTES_READ]; 
    struct sockaddr_in servaddr, cliaddr; 
      
    // Creating socket file descriptor 
    if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 )
    { 
        perror("socket"); 
        exit(1); 
    } 
      
    memset(&servaddr, 0, sizeof(servaddr)); 
    memset(&cliaddr, 0, sizeof(cliaddr)); 
      
    // Filling server information 
    servaddr.sin_family    = AF_INET; // IPv4 
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1"); 
    servaddr.sin_port = htons(atoi(port)); 
      
    // Bind the socket with the server address 
    if ( bind(sockfd, (const struct sockaddr *)&servaddr,  
            sizeof(servaddr)) < 0 ) 
    { 
        perror("bind"); 
        exit(1); 
    } 
      
    int len, n; 
    n = recvfrom(sockfd, (char *)buffer, MAX_BYTES_READ, 0, ( struct sockaddr *) NULL, 0); 
    buffer[n] = '\0'; 
    printf("Client : %s\n", buffer); 
    PrintHex(buffer, n);

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
