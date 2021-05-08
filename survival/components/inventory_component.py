class InventoryComponent:
    def __init__(self, maxitems):
        self.maxitems = maxitems
        self.items = {}

    def addItem(self, item, count):
        if item not in self.items:
            self.items[item] = count
        else:
            self.items[item] = self.items[item] + count
        if self.items[item] > self.maxitems:
            self.items[item] = self.maxitems

    def removeItem(self, item, count):
        if self.items:
            self.items[item] = self.items[item] - count
        if self.items[item] < 0:
            self.items[item] = 0

    def hasItem(self, item):
        if self.items[item] != 0:
            return True
        else:
            return False
