import time

from reutils.logging import Logger

logger = Logger(__name__)

if __name__ == '__main__':
    with logger.progress(10, 'Progress') as p:
        for i in range(10):
            time.sleep(2)
            p.update(i + 1)

