import time

from reutils import parallel


def sq(x):
    return x ** x


if __name__ == '__main__':
    then = time.time()
    map(sq, range(5, int(1e5)))
    now = time.time()
    print(now - then)

    then = time.time()
    map(sq, list(range(5, int(1e5))))
    now = time.time()
    print(now - then)

    then = time.time()
    parallel.map(sq, range(5, int(1e5)), 2)
    now = time.time()
    print(now - then)
