import datetime
import logging

__all__ = [
    'Logger',
]

LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=LOGGING_FORMAT)

NOTSET = logging.NOTSET
INFO = logging.INFO
DEBUG = logging.DEBUG
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


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

    def progress_bar(self, size=0, desc=None):
        temp = Progress(size, desc)
        temp.print = self.print_func
        return temp

    @property
    def p(self):
        return self.progress_bar

    def __call__(self, items, size=None, desc=None):
        if size is None:
            size = len(items)
        with self.progress_bar(size, desc) as p:
            for i, item in enumerate(items):
                yield item
                p.update(i + 1)


class Logger(logging.Logger):
    def __init__(self, name=None, level=logging.NOTSET):
        super().__init__(name, level)

    @property
    def progress(self):
        return ProgressLogger(self)


def getLogger(name=None):
    logging_class = logging.getLoggerClass()
    logging._acquireLock()
    try:
        logging.setLoggerClass(Logger)
        logger = logging.getLogger(name)
        logging.setLoggerClass(logging_class)
        return logger
    finally:
        logging._releaseLock()


def basicConfig(**kwargs):
    logging.basicConfig(**kwargs)
