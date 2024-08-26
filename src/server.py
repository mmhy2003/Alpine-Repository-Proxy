#!/bin/env python3
import os
import logging
import requests
from flask import Flask
from datetime import datetime, timedelta
from threading import Lock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('alpine-proxy')

# Create the Flask app
app = Flask(__name__)

# Public Variables
CACHE_DIR = os.getenv('CACHE_DIR', 'cache')
PORT = int(os.getenv('PORT', '8654'))
INDEX_CACHE_EXPIRY_DAYS = int(os.getenv('INDEX_CACHE_EXPIRY_DAYS', '1'))

ALPINE_REMOTES = os.getenv('ALPINE_REMOTES', '')
alpine_remotes = {
    "default": "https://dl-cdn.alpinelinux.org",
}
if ALPINE_REMOTES:
    alpine_remotes.update({k: v for k, v in (item.split("::") for item in ALPINE_REMOTES.split(","))})

# Dictionary to store locks for each file path
file_locks = {}


# Helper Functions
def download_file(path):
    remote = path.split('/')[0]
    remote_path = '/'.join(path.split('/')[1:])
    file_path = f'{CACHE_DIR}/{remote}/{remote_path}'
    dir_path = os.path.dirname(file_path)
    url = alpine_remotes[remote] + '/' + remote_path

    # Fetch the file
    response = requests.get(url)

    # Write the file to the cache directory
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, 'wb') as file:
        file.write(response.content)


def fetch_cache(path):
    repo = path.split('/')[0]
    remote_path = '/'.join(path.split('/')[1:])
    file_path = f'{CACHE_DIR}/{repo}/{remote_path}'
    metadata_path = f'{file_path}.meta'

    # Ensure only one thread can download the file at a time
    if file_path not in file_locks:
        file_locks[file_path] = Lock()

    with file_locks[file_path]:
        try:
            # Download Index file
            if 'APKINDEX.tar.gz' in path:
                if not os.path.exists(file_path) or not os.path.exists(metadata_path):
                    download_file(path)
                else:
                    with open(metadata_path, 'r') as meta_file:
                        cached_time = datetime.fromisoformat(meta_file.read().strip())
                        if datetime.now() - cached_time > timedelta(days=INDEX_CACHE_EXPIRY_DAYS):
                            download_file(path)
                with open(metadata_path, 'w') as meta_file:
                    meta_file.write(datetime.now().isoformat())

            # Download package
            elif not os.path.exists(file_path):
                download_file(path)

            # Return the file
            with open(file_path, 'rb') as f:
                return f.read()

        except FileNotFoundError:
            pass


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    file = fetch_cache(path)
    return file, 200


if __name__ == '__main__':
    os.makedirs(CACHE_DIR, exist_ok=True)
    logger.info(f'Cache directory created at: {CACHE_DIR}')

    logger.info('# Alpine Remotes Repositories:')
    for key, value in alpine_remotes.items():
        logger.info(f'------ http://localhost:{PORT}/{key}/ -> {value}')

    app.run(host='0.0.0.0', port=PORT)
