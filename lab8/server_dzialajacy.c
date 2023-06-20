#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

#define TCP_PORT 8080             // TCP server port
#define UDP_PORT 9090             // UDP multicast server port
#define MULTICAST_GROUP "239.0.0.1"
#define BUFFER_SIZE 1024

void handlePrivateChat(int clientSocket, int udpSocket, struct sockaddr_in multicastAddr);
void handleGroupChat(int udpSocket);

int main(int argc, char *argv[]) {
    int tcpServerSocket, udpServerSocket, clientSocket;
    struct sockaddr_in tcpServerAddress, udpServerAddress, clientAddress;
    char buffer[BUFFER_SIZE];
    socklen_t clientAddressLength;

    // Check if a multicast group address was given
    if (argc != 2) {
        printf("Please give a multicast address as an argument\n");
        return 1;
    }
    char *group = argv[1];

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

    u_int yes = 1;
    if (
        setsockopt(
            udpServerSocket, SOL_SOCKET, SO_REUSEADDR, (char*) &yes, sizeof(yes)
        ) < 0
    ){
       perror("Reusing ADDR failed");
       return 1;
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

    // Configure multicast address
    struct sockaddr_in multicastAddr;
    memset(&multicastAddr, 0, sizeof(multicastAddr));
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
    if (setsockopt(udpServerSocket, IPPROTO_IP, IP_ADD_MEMBERSHIP, (void *)&multicastRequest, sizeof(multicastRequest)) < 0) {
        perror("Joining multicast group failed");
        exit(EXIT_FAILURE);
    }

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
            close(tcpServerSocket);  // Child process doesn't need to listen for new connections
            handlePrivateChat(clientSocket, udpServerSocket, multicastAddr);
            close(clientSocket);
            exit(EXIT_SUCCESS);
        } else {
            close(clientSocket);  // Parent process doesn't need this client socket
        }
    }

    // Close the TCP and UDP sockets
    close(tcpServerSocket);
    close(udpServerSocket);

    return 0;
}

void handlePrivateChat(int clientSocket, int udpSocket, struct sockaddr_in multicastAddr) {
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

	// Send the message to multicast group
        if (sendto(udpSocket, buffer, strlen(buffer), 0, (struct sockaddr *)&multicastAddr, sizeof(multicastAddr)) < 0) {
	    perror("Error sending UDP message");
	    exit(EXIT_FAILURE);
	}


        // Clear the buffer
        memset(buffer, 0, BUFFER_SIZE);
    }
}

