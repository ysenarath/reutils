import datetime
import logging
import time

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)


def _cls_print(message):
    print('\r{}'.format(message), end='')


class Progress:
    def __init__(self, size=0, desc=None):
        if desc is None:
            desc = 'Progress'
        self.size = size
        self.desc = desc
        self.print = _cls_print
        self._update_time = None
        self._update_freq = datetime.timedelta(seconds=2)

    def __enter__(self):
        self.update(0)
        return self

    # noinspection SpellCheckingInspection
    def update(self, v):
        pval = int(v * 100 / self.size)
        update_time = datetime.datetime.now()
        if (self._update_time is None) or (update_time >= self._update_time):
            np = int(pval / 5)
            message = '{} {:>3}% [{}{}]'.format(self.desc, pval, '#' * np, '-' * (20 - np))
            self.print(message)
            self._update_time = update_time + self._update_freq

    # noinspection PyMethodMayBeStatic
    def __exit__(self, type, value, traceback):
        self._update_time = None
        self.update(self.size)


class Logger:
    def __init__(self, name='Unknown', level=1):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

    def log(self, level, message):
        self.logger.log(level, message)

    def info(self, message):
        self.logger.info(message)

    def status(self, message, status):
        self.info('{} [{}]'.format(message, status.upper()))

    # noinspection PyMethodMayBeStatic,SpellCheckingInspection
    def progress(self, size=0, desc=None):
        prog = Progress(size, desc)
        prog.print = self.info
        return prog


if __name__ == '__main__':
    logger = Logger(__name__)
    logger.status('Initializing program...', 'starting')
    with logger.progress(10) as p:
        for i in range(11):
            p.update(i)
            time.sleep(10)
    logger.status('Initializing program...', 'complete')
