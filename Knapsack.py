from Item import Item
import numpy as np


class Knapsack:
    def __init__(self, N, max_weight, max_value, capacity):
        self.items = np.array([Item(max_weight, max_value) for _ in range(N)])
        self.value = 0
        self.mass = 0
        self.capacity = capacity

    def compute_value(self):
        """
        Computes value of items taken.
        """
        self.value = 0
        for item in self.items:
            if item.taken == 1:
                self.value += item.value

    def compute_mass(self):
        """
        Computes mass of items taken, and randomly discards items
        if mass is too high.
        """
        self.mass = 0
        for item in self.items:
            if item.taken == 1:
                self.mass += item.weight
        while self.mass > self.capacity:  # Takes care of mass limit
            index = np.random.randint(len(self.items))
            if self.items[index].taken == 1:
                self.items[index].taken = 0

    def __str__(self):
        return f'V:{self.value} M:{self.mass}'
