import random

from survival.generators.resource_type import ResourceType


class ResourceComponent:
    def __init__(self, resource_type):
        self.resource_type = resource_type
        w, e, t = self.generate_attributes(resource_type)
        self.weight = w
        self.eatable = e
        self.toughness = t

    @staticmethod
    def generate_attributes(resource_type):
        if resource_type == ResourceType.WOOD:
            weight = random.randint(10, 15)
            eatable = False
            toughness = random.randint(10, 15)
        elif resource_type == ResourceType.WATER:
            weight = random.randint(1, 2)
            eatable = True
            toughness = 0
        else:
            weight = random.randint(1, 7)
            eatable = True
            toughness = random.randint(2, 5)

        return weight, eatable, toughness
