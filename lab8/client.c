#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <fcntl.h>

#define TCP_PORT 8080             // TCP server port
#define UDP_PORT 9090             // UDP multicast server port
#define MULTICAST_GROUP "239.0.0.1"
#define BUFFER_SIZE 1024

int main() {
    int tcpSocket, udpSocket;
    struct sockaddr_in serverAddr, udpAddr;
    char tcpBuffer[BUFFER_SIZE], udpBuffer[BUFFER_SIZE];

    // Create TCP socket
    if ((tcpSocket = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("TCP socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Create UDP socket
    if ((udpSocket = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
        perror("UDP socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Set SO_REUSEADDR option for TCP socket
    int reuse = 1;
    if (setsockopt(tcpSocket, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) == -1) {
        perror("TCP setsockopt(SO_REUSEADDR) failed");
        exit(EXIT_FAILURE);
    }

    // Set SO_REUSEADDR option for UDP socket
    if (setsockopt(udpSocket, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) == -1) {
        perror("UDP setsockopt(SO_REUSEADDR) failed");
        exit(EXIT_FAILURE);
    }

    // Configure server address for TCP connection
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(TCP_PORT);

    // Connect TCP socket to the server
    if (connect(tcpSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0) {
        perror("TCP connection failed");
        exit(EXIT_FAILURE);
    }

    // Configure UDP address for multicast group
    udpAddr.sin_family = AF_INET;
    udpAddr.sin_port = htons(UDP_PORT);
    if (inet_pton(AF_INET, MULTICAST_GROUP, &(udpAddr.sin_addr)) <= 0) {
        perror("Invalid multicast group address");
        exit(EXIT_FAILURE);
    }

    // Join the UDP multicast group
    struct ip_mreq mreq;
    mreq.imr_multiaddr.s_addr = inet_addr(MULTICAST_GROUP);
    mreq.imr_interface.s_addr = htonl(INADDR_ANY);
    if (setsockopt(udpSocket, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, sizeof(mreq)) == -1) {
        perror("Joining multicast group failed");
        exit(EXIT_FAILURE);
    }

    while (1) {
        // Send message over TCP
        printf("Enter a message to send over TCP: ");
        fgets(tcpBuffer, BUFFER_SIZE, stdin);
        send(tcpSocket, tcpBuffer, strlen(tcpBuffer), 0);

        // Receive message over UDP
        ssize_t bytesRead = recv(udpSocket, udpBuffer, BUFFER_SIZE, 0);
        if (bytesRead > 0) {
            udpBuffer[bytesRead] = '\0';
            printf("Received message over UDP: %s\n", udpBuffer);
        }

        // Wait for a while before the next iteration
        sleep(1);
    }

    // Close sockets
    close(tcpSocket);
    close(udpSocket);

    return 0;
}