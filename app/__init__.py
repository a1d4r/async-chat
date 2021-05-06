import logging
import sys

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO,
    stream=sys.stdout,
)
