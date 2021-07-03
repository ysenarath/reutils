import time

from reutils import logging_v2 as logging

logging.basicConfig(format=logging.LOGGING_FORMAT)

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

if __name__ == '__main__':
    logger.error('Hello from example.')
    items = list(range(10))
    for _ in logger.progress(items):
        time.sleep(1)
    with logger.progress.p(len(items), 'Progress') as p:
        for i, _ in enumerate(items):
            time.sleep(1)
            p.update(i + 1)
