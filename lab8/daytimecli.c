#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#define MAXLINE 1023
#define SA      struct sockaddr

int main(int argc, char **argv)
{
    int sockfd, n;
    struct sockaddr_in6 servaddr;
    char recvline[MAXLINE + 1];
    int err;
    char username[20];

    if (argc != 2) {
        fprintf(stderr, "ERROR: usage: a.out <IPaddress>\n");
        return 1;
    }

    printf("Enter your username: ");
    fgets(username, sizeof(username), stdin);
    // remove newline character from username
    username[strcspn(username, "\n")] = 0;

    if ((sockfd = socket(AF_INET6, SOCK_STREAM, 0)) < 0) {
        fprintf(stderr, "socket error: %s\n", strerror(errno));
        return 1;
    }

    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin6_family = AF_INET6;
    servaddr.sin6_port = htons(13); /* daytime server */
    if ((err = inet_pton(AF_INET6, argv[1], &servaddr.sin6_addr)) <= 0) {
        if (err == 0)
            fprintf(stderr, "inet_pton error for %s\n", argv[1]);
        else
            fprintf(stderr, "inet_pton error for %s: %s\n", argv[1], strerror(errno));
        return 1;
    }
    if (connect(sockfd, (SA *)&servaddr, sizeof(servaddr)) < 0) {
        fprintf(stderr, "connect error: %s\n", strerror(errno));
        return 1;
    }

    // send username to server
    if (write(sockfd, username, strlen(username)) < 0) {
        fprintf(stderr, "write error: %s\n", strerror(errno));
        return 1;
    }

    while ((n = read(sockfd, recvline, MAXLINE)) > 0) {
        recvline[n] = 0; /* null terminate */
        if (fputs(recvline, stdout) == EOF) {
            fprintf(stderr, "fputs error: %s\n", strerror(errno));
            return 1;
        }
    }

    if (n < 0)
        fprintf(stderr, "read error: %s\n", strerror(errno));

    fflush(stdout);
    fprintf(stderr, "\nOK\n");

    exit(0);
}