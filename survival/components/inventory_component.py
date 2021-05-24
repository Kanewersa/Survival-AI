class InventoryComponent:
    def __init__(self, maxitems=100):
        self.maxitems = maxitems
        self.items = {}

    def add_item(self, item, count):
        if item not in self.items:
            self.items[item] = count
        else:
            self.items[item] = self.items[item] + count
        if self.items[item] > self.maxitems:
            self.items[item] = self.maxitems

    def remove_item(self, item, count):
        if item in self.items:
            self.items[item] = self.items[item] - count
            if self.items[item] < 0:
                self.items[item] = 0

    def has_item(self, item):
        return item in self.items and self.items[item] != 0
