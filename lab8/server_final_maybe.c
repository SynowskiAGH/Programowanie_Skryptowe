#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

#define TCP_PORT 8080             // TCP server port
#define UDP_PORT 9090             // UDP multicast server port
#define BUFFER_SIZE 1024

void handlePrivateChat(int clientSocket);
void handleGroupChat(int udpSocket);

int main(int argc, char *argv[]) {  // Added argc and argv[] parameters
    int tcpServerSocket, udpServerSocket, clientSocket;
    struct sockaddr_in tcpServerAddress, udpServerAddress, clientAddress;
    char buffer[BUFFER_SIZE];
    socklen_t clientAddressLength;

    // Check if a multicast group address was given
    if (argc != 2) {
       printf("Please give a multicast address as an argument\n");
       return 1;
    }
    char* group = argv[1];

    // Create a socket for multicast UDP
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) {
        perror("Error creating the multicast socket");
        return 1;
    }
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr(group);
    addr.sin_port = htons(UDP_PORT);

    // Create TCP socket
    tcpServerSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (tcpServerSocket == -1) {
        perror("Error creating TCP socket");
        exit(EXIT_FAILURE);
    }

    // Create UDP socket
    udpServerSocket = socket(AF_INET, SOCK_DGRAM, 0);
    if (udpServerSocket == -1) {
        perror("Error creating UDP socket");
        exit(EXIT_FAILURE);
    }

    // Set up TCP server address
    tcpServerAddress.sin_family = AF_INET;
    tcpServerAddress.sin_addr.s_addr = INADDR_ANY;
    tcpServerAddress.sin_port = htons(TCP_PORT);

    // Bind the TCP socket to the TCP server address
    if (bind(tcpServerSocket, (struct sockaddr *)&tcpServerAddress, sizeof(tcpServerAddress)) < 0) {
        perror("TCP socket binding failed");
        exit(EXIT_FAILURE);
    }

    // Set up UDP server address
    udpServerAddress.sin_family = AF_INET;
    udpServerAddress.sin_addr.s_addr = INADDR_ANY;
    udpServerAddress.sin_port = htons(UDP_PORT);

    // Bind the UDP socket to the UDP server address
    if (bind(udpServerSocket, (struct sockaddr *)&udpServerAddress, sizeof(udpServerAddress)) < 0) {
        perror("UDP socket binding failed");
        exit(EXIT_FAILURE);
    }

    printf("Server started. Waiting for connections...\n");

    // Listen for TCP connections
    if (listen(tcpServerSocket, 5) < 0) {
        perror("TCP listen failed");
        exit(EXIT_FAILURE);
    }

    // Accept TCP connections and handle private chat
    while (1) {
        clientAddressLength = sizeof(clientAddress);

        // Accept TCP connection from a client
        clientSocket = accept(tcpServerSocket, (struct sockaddr *)&clientAddress, &clientAddressLength);
        if (clientSocket < 0) {
            perror("TCP accept failed");
            exit(EXIT_FAILURE);
        }

        printf("New client connected: %s\n", inet_ntoa(clientAddress.sin_addr));

        // Fork a child process to handle private chat
        if (fork() == 0) {
            handlePrivateChat(clientSocket);
            close(clientSocket);
            exit(EXIT_SUCCESS);
        } else {
            close(clientSocket);
        }
    }

    // Close the TCP and UDP sockets
    close(tcpServerSocket);
    close(udpServerSocket);
    close(fd);

    return 0;
}

void handlePrivateChat(int clientSocket) {
    char buffer[BUFFER_SIZE];
    int bytesRead;

    while (1) {
        // Receive a message from the client
        bytesRead = recv(clientSocket, buffer, BUFFER_SIZE, 0);
        if (bytesRead <= 0) {
            printf("Client disconnected\n");
            break;
        }

        // Null-terminate the received message
        buffer[bytesRead] = '\0';

        // Print the received message
        printf("Received from client: %s\n", buffer);

        // Forward the message to the multicast group if anything was received
        if (bytesRead > 0) {
            char ch = 0;
            int nbytes = sendto(
                fd,
                buffer,
                strlen(buffer),
                0,
                (struct sockaddr*) &addr,
                sizeof(addr)
            );
            if (nbytes < 0) {
                perror("sendto");
                exit(EXIT_FAILURE);
            }
        }

        // Clear the buffer
        memset(buffer, 0, BUFFER_SIZE);
    }
}

void handleGroupChat(int udpSocket) {
    struct sockaddr_in clientAddress;
    char buffer[BUFFER_SIZE];
    socklen_t clientAddressLength;
    int bytesRead;

    while (1) {
        clientAddressLength = sizeof(clientAddress);

        // Receive a message from a client in the group
        bytesRead = recvfrom(udpSocket, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&clientAddress, &clientAddressLength);
        if (bytesRead <= 0) {
            perror("Error receiving UDP message");
            exit(EXIT_FAILURE);
        }

        // Null-terminate the received message
        buffer[bytesRead] = '\0';

        // Print the received message and client information
        printf("Received from client (%s:%d): %s\n", inet_ntoa(clientAddress.sin_addr), ntohs(clientAddress.sin_port), buffer);

        // Send a response to the client
        char ch = 0;
        int nbytes = sendto(
            fd,
            buffer,
            strlen(buffer),
            0,
            (struct sockaddr*) &addr,
            sizeof(addr)
        );
        if (nbytes < 0) {
            perror("sendto");
            exit(EXIT_FAILURE);
        }

        // Clear the buffer
        memset(buffer, 0, BUFFER_SIZE);
    }
}
