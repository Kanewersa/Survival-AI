from enum import Enum


class ResourceType(Enum):
    FOOD = 1
    WATER = 2
    WOOD = 3

    @staticmethod
    def get_from_string(string):
        if string == 'food':
            return ResourceType.FOOD
        elif string == 'water':
            return ResourceType.WATER
        elif string == 'wood':
            return ResourceType.WOOD
        else:
            raise Exception("Unknown resource type")
