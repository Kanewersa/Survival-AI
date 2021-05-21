class OnCollisionComponent:
    def __init__(self, callbacks: [] = []):
        self.callbacks = callbacks

    def callAll(self):
        for func in self.callbacks:
            func()

    def addCallback(self, fn):
        self.callbacks.append(fn)