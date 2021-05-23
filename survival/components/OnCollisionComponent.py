from functools import partial


class OnCollisionComponent:
    def __init__(self, callbacks=None):
        if callbacks is None:
            callbacks = []
        self.callbacks = callbacks

    def callAll(self):
        for func in self.callbacks:
            func()

    def addCallback(self, fn, **kwargs):
        self.callbacks.append(partial(fn, **kwargs))
