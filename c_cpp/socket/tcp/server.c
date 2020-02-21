#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <stdlib.h>

#define PORT    7892
#define MAXLINE 1024

int main(){
    int welcomeSocket, newSocket, portNum, clientLen, nBytes;
    char buffer[MAXLINE];
    struct sockaddr_in serverAddr;
    struct sockaddr_storage serverStorage;
    socklen_t addr_size;
    int i;

    welcomeSocket = socket(PF_INET, SOCK_STREAM, 0);

    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(PORT);
    serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
    memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero);

    bind(welcomeSocket, (struct sockaddr *) &serverAddr, sizeof(serverAddr));

    if (listen(welcomeSocket, 5) == 0) {
        printf("Listening...\n");
    }
    else {
        printf("Error\n");
    }

    addr_size = sizeof serverStorage;

    /*loop to keep accepting new connections*/
    while(1) {
        newSocket = accept(welcomeSocket, (struct sockaddr *) &serverStorage, &addr_size);
        printf("New client(%d) connecting...\n", newSocket);
        /*fork a child process to handle the new connection*/
        if (!fork()) {
            nBytes = 1;
            /*loop while connection is live*/
            while (nBytes != 0) {
                memset(buffer, 0, sizeof(buffer));
                nBytes = recv(newSocket, buffer, MAXLINE, 0);
                printf("Received from client(%d): %s\n", newSocket, buffer);
                send(newSocket, buffer, nBytes, 0);
                memset(buffer, 0, sizeof(buffer));
            }
            printf("Client(%d) closing...\n", newSocket);
            close(newSocket);
            exit(0);
        }
        /*if parent, close the socket and go back to listening new requests*/
        else {
            close(newSocket);
        }
    }

    return 0;
}
