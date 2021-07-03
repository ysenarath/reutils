import typing
from multiprocessing import Process, Pipe, connection

from reutils.iterutils import chunk

__all__ = [
    'map'
]


class Function:
    def __init__(self, fun: typing.Callable):
        self.fun: typing.Callable = fun

    def __call__(self, conn: connection.Connection, data: typing.Any):
        results = [self.fun(item) for item in data]
        conn.send(results)
        conn.close()


def map(fun: typing.Callable, iter: typing.Any, workers: int = 4) -> typing.List:
    """`parallel.map()` function returns the results after applying the given function
     to each item of a given iterable with provided number of workers.

    :param fun: function to which map passes each element of given iterable.
    :param iter: iterable which is to be mapped.
    :param workers: number of processes to do the work.
    :return: list of the results after applying the given function to each item of a given iterable.
    """
    processes = []
    items = chunk(iter, workers)
    for i, data in enumerate(items):
        parent_conn, child_conn = Pipe()
        process = Process(target=Function(fun), args=(child_conn, data))
        processes.append((process, parent_conn))
    results = []
    for p, c in processes:
        p.start()
        results += c.recv()
    for p, _ in processes:
        p.join()
    return results
