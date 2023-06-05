#!/bin/bash

set -e

# Check if the environment mode is DEV
if [ "$LOCAL_DEV_MODE" == "TRUE" ]; then
    apt update -y && apt upgrade -y 
    apt install -y libnss3-tools curl
    curl -JLO "https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64" && chmod +x mkcert-v*-linux-amd64 && cp mkcert-v*-linux-amd64 /usr/local/bin/mkcert

    mkcert -install
    mkcert localhost 127.0.0.1 ::1
    mv localhost+2.pem cert.pem
    mv localhost+2-key.pem key.pem
fi