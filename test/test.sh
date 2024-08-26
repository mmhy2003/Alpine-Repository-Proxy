#!/bin/bash

# Get enp0s3 IP address
ip=$(ip -4 addr show enp0s3 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
echo "Your Machine IP Address: $ip" && \

# Build & Run test
echo "### Building & Running test... ###" && \
docker build -t alpine-proxy-test . && \
docker run --rm --add-host dev-machine:$ip alpine-proxy-test apk add --no-cache wireshark && \
echo "### Run test again to check cache... ###" && \
docker run --rm --add-host dev-machine:$ip alpine-proxy-test apk add --no-cache wireshark