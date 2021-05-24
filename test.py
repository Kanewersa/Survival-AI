import random


def generate_data():
    f = open("data.txt", "w")
    for i in range(1000):
        weight = random.randint(0, 11)
        eatable = bool(random.randint(0, 1))
        toughness = random.randint(0, 3)
        f.write('{')
        f.write(
            f'"weight": {weight}, "eatable": {str(eatable).lower()}, "toughness": {toughness}, "resource": "{get_resource_type(weight, eatable, toughness)}"')
        f.write('}')
        f.write('\n')
    f.close()


def get_resource_type(weight, eatable, toughness):
    if weight > 10 or eatable is False:
        return "wood"

    if toughness < 1:
        return "water"

    return "food"


generate_data()
