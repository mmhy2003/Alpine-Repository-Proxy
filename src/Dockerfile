FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

# Set the working directory
WORKDIR /app

# Set the environment variables
ENV PYTHONUNBUFFERED=1
ENV CACHE_DIR=cache
ENV PORT=8654
ENV INDEX_CACHE_EXPIRY_DAYS=1

# Volume for the cache
VOLUME /app/cache

# Install the required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt /app/requirements.txt

# Install the required python packages
RUN pip3 install --no-cache-dir -U pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy the server file
COPY server.py /app

# Expose the port
EXPOSE 8654

# Run the server
CMD ["python3", "server.py"]