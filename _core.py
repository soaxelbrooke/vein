
from inspect import getargspec
from collections import deque


class Vein(object):
    def __init__(self, function, subscribers=None):
        self.sources = {name: deque() for name in getargspec(function).args}
        self.function = function
        self._subscribers = subscribers or {}

    def send(self, named_item):
        name, item = named_item
        self.sources[name].append(item)
        self.flush()

    def emit(self, item):
        print(item)
        for sink, argname in self._subscribers.items():
            sink.send((argname, item))

    def subscribers(self, subs):
        self._subscribers.update(subs)

    @property
    def inputs(self):
        while all(map(lambda source: len(source) > 0, self.sources.values())):
            yield {name: self.sources[name].popleft() for name in self.sources}

    def flush(self):
        # Process as many inputs as possible
        for kwargs in self.inputs:
            self.emit(self.function(**kwargs))


mul = Vein(lambda n, m: n * m)
inc = Vein(lambda n: n + 1, subscribers={mul: 'm'})

mul.send(('n', 3))
inc.send(('n', 5))
#mul.send(('m', 7))
