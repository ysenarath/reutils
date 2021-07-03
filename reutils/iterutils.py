import math


def chunk(iterable, splits=4):
    results = list(iterable)
    size_of_split = math.ceil(len(results) / splits)
    for idx in range(0, len(results), size_of_split):
        yield results[idx:idx + size_of_split]


if __name__ == '__main__':
    print(list(chunk(list(range(20)), 100)))
