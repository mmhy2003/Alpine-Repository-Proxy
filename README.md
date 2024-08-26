# Alpine Repository Proxy

## Overview

This project provides a proxy server for Alpine Linux repositories. It caches repository index files and packages to reduce bandwidth usage and improve access speed. The proxy server is built using Flask and caches files locally.

## Features

- **Caching**: Caches repository index files and packages to reduce redundant downloads.
- **Thread Safety**: Ensures that only one thread can download a file at a time using locks.
- **Configurable**: Allows configuration of cache directory, port, and cache expiry through environment variables.

## Environment Variables

- `CACHE_DIR`: Directory where cached files are stored (default: `cache`).
- `PORT`: Port on which the proxy server runs (default: `8654`).
- `INDEX_CACHE_EXPIRY_DAYS`: Number of days before the index cache expires (default: `1`).
- `ALPINE_REMOTES`: Comma-separated list of Alpine remotes in the format `name::url`.

## Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/mmhy2003/Alpine-Repository-Proxy.git
    cd Alpine-Repository-Proxy
    ```

2. **Install dependencies**:
    ```sh
    pip install -r src/requirements.txt
    ```

3. **Run the server**:
    ```sh
    python src/server.py
    ```

## Usage

### Running the Proxy Server

Start the proxy server by running the `src/server.py` script. The server will listen on the port specified by the `PORT` environment variable (default: `8654`).

### Configuring Alpine to Use the Proxy

To configure an Alpine Linux system to use the proxy, modify the `/etc/apk/repositories` file to point to the proxy server. For example:

http://localhost:8654/alpine

### Testing

A Docker-based test setup is provided to verify the proxy server's functionality.

1. **Build and run the test**:
    ```sh
    test/test.sh
    ```

This script will:
- Retrieve the IP address of the `enp0s3` network interface.
- Build a Docker image using the provided `test/Dockerfile`.
- Run a container from the built image and install a package (`wireshark`) using `apk`.
- Run the container again to check if the package is served from the cache.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.