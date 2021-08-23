import logging
import sys
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# List of VirtServers in the cluster
VIRTSERVERS = [
    '10.0.10.1',
    '10.0.10.2'
]

# VirtServers credentials, create the same user with password on all VirtServers
VIRTSERVER_USER = os.environ['USER']
VIRTSERVER_PASSWORD = os.environ['PASSWORD']

# VirtServer CLI path
VIRTSERVER_CLI = '/usr/local/bin/virtserver-cli.sh'

# Traefik URL
TRAEFIK_URL = 'mock.example.com'
