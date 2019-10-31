import numpy as np


class Item:
    def __init__(self, max_weight, max_value):
        self.weight = np.random.randint(1, max_weight+1)
        self.value = np.random.randint(1, max_value)
        self.taken = np.random.randint(0, 2)

    def __str__(self):
        return self.taken
