#!/bin/bash

gcc -Wall -lssl -lcrypto -o out/ssl-demo ssl-demo.c
gcc -lssl -lcrypto -o out/sslconnect sslconnect.c
gcc -lssl -lcrypto -o out/ssl_client ssl_client.c
