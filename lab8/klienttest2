#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netinet/in.h>

#define TCP_PORT 8080             // TCP server port
#define UDP_PORT 9090             // UDP multicast server port
#define MULTICAST_GROUP "239.0.0.1"
#define BUFFER_SIZE 1024

void handleMulticast(int udpSocket);

int main() {
    int tcpSocket, udpSocket;
    struct sockaddr_in serverAddress;
    char buffer[BUFFER_SIZE];
    ssize_t bytesRead;

    // Create TCP socket
    tcpSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (tcpSocket == -1) {
        perror("Error creating TCP socket");
        exit(EXIT_FAILURE);
    }

    // Create UDP socket
    udpSocket = socket(AF_INET, SOCK_DGRAM, 0);
    if (udpSocket == -1) {
        perror("Error creating UDP socket");
        exit(EXIT_FAILURE);
    }

    // Set up server address
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(TCP_PORT);
    if (inet_aton("127.0.0.1", &serverAddress.sin_addr) == 0) {
        perror("Invalid server address");
        exit(EXIT_FAILURE);
    }

    // Connect to the server
    if (connect(tcpSocket, (struct sockaddr *)&serverAddress, sizeof(serverAddress)) < 0) {
        perror("TCP connection failed");
        exit(EXIT_FAILURE);
    }

    printf("Connected to server. Enter 'q' to quit.\n");

    // Create child process to handle multicast
    if (fork() == 0) {
        handleMulticast(udpSocket);
        exit(EXIT_SUCCESS);
    }

    // Send messages to the server
    while (1) {
        // Read input from the user
        fgets(buffer, BUFFER_SIZE, stdin);

        // Remove newline character
        buffer[strcspn(buffer, "\n")] = '\0';

        // Check if user wants to quit
        if (strcmp(buffer, "q") == 0) {
            break;
        }

        // Send the message to the server
        if (send(tcpSocket, buffer, strlen(buffer), 0) < 0) {
            perror("Error sending TCP message");
            exit(EXIT_FAILURE);
        }
    }

    // Close the TCP and UDP sockets
    close(tcpSocket);
    close(udpSocket);

    return 0;
}

void handleMulticast(int udpSocket) {
    struct sockaddr_in multicastAddr;
    char buffer[BUFFER_SIZE];
    ssize_t bytesRead;

    // Set up multicast address
    multicastAddr.sin_family = AF_INET;
    multicastAddr.sin_port = htons(UDP_PORT);
    if (inet_aton(MULTICAST_GROUP, &multicastAddr.sin_addr) == 0) {
        perror("Invalid multicast address");
        exit(EXIT_FAILURE);
    }

    // Join the multicast group
    struct ip_mreq multicastRequest;
    multicastRequest.imr_multiaddr.s_addr = inet_addr(MULTICAST_GROUP);
    multicastRequest.imr_interface.s_addr = htonl(INADDR_ANY);
    if (setsockopt(udpSocket, IPPROTO_IP, IP_ADD_MEMBERSHIP, (void *)&multicastRequest, sizeof(multicastRequest)) < 0) {
        perror("Joining multicast group failed");
        exit(EXIT_FAILURE);
    }

    // Receive messages from the multicast group
    while (1) {
        // Clear the buffer
        memset(buffer, 0, BUFFER_SIZE);

        // Receive a message from the multicast group
        bytesRead = recvfrom(udpSocket, buffer, BUFFER_SIZE, 0, NULL, NULL);
        if (bytesRead < 0) {
            perror("Error receiving UDP message");
            exit(EXIT_FAILURE);
        }

        // Print the received message
        printf("Received from multicast: %s\n", buffer);
    }
}
