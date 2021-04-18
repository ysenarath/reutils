import datetime
import logging

__all__ = [
    'Logger',
]

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
        self._message = None

    def __enter__(self):
        self.update(0)
        return self

    # noinspection SpellCheckingInspection
    def update(self, v):
        pval = int(v * 100 / self.size)
        update_time = datetime.datetime.now()
        if (self._update_time is None) or (update_time >= self._update_time):
            np = int(pval / 5)
            self._message = '{} {:>3}% [{}{}]'.format(self.desc, pval, '#' * np, '-' * (20 - np))
            if self.print is not None:
                self.print(self._message)
            self._update_time = update_time + self._update_freq

    def __str__(self):
        return self._message

    # noinspection PyMethodMayBeStatic
    def __exit__(self, type, value, traceback):
        self._update_time = None
        self.update(self.size)


class ProgressLogger:
    def __init__(self, logger):
        self.logger = logger
        self.print_func = self.logger.info

    def __getattr__(self, item):
        self.print_func = getattr(self.logger, item)
        return self

    def __call__(self, size=0, desc=None):
        progress_bar = Progress(size, desc)
        progress_bar.print = self.print_func
        return progress_bar


class Logger:
    def __init__(self, name='Unknown', level=1):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

    def __getattr__(self, item):
        return getattr(self.logger, item)

    def status(self, message, status):
        self.logger.info('{} [{}]'.format(message, status.upper()))

    @property
    def progress(self):
        return ProgressLogger(self.logger)


def main():
    logger = Logger()
    with logger.progress(10) as p:
        for x in range(1, 10):
            p.update(x)
