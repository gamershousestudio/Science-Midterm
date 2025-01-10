# Code created by chatgpt
# Used as an itertools.batched alternitave

from itertools import islice

class Batched:
    def batched(iterable, batch_size):
        iterator = iter(iterable)
        for first in iterator:
            yield list(islice([first] + list(iterator), batch_size))
