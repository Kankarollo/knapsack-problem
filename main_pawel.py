# 0-1 knapsack problem using genetic algorithm
# with (mu + lambda) evolution strategy
# http://www.scholarpedia.org/article/Evolution_strategies
# https://www.tutorialspoint.com/genetic_algorithms/index.htm

import matplotlib.pyplot as plt
import numpy as np
import copy
from Knapsack import Knapsack
from Enums import ParentSelection, MutationSelection

# Config
N = 100  # Number of items [100, 250, 500]
capacity = N * 3
max_value = 20
max_weight = 10

pop_size = 20  # mu
epochs = 200
num_offspring = 140  # lambda
num_breeding_parents = 20  # p
mutation_chance = 1.0  # Chance of mutation to occur

mutation_type = MutationSelection.Flip
# End of config


def populate(num_genes, pop_size, max_weight, max_value, capacity):
    return np.array([Knapsack(num_genes, max_weight, max_value, capacity) for _ in range(pop_size)])

def mutate(pops):
    offspring = []
    for _ in range(num_offspring):
        offspring.append(copy.copy(pops[np.random.randint(0,len(pops))]))
    for kid in offspring:
        if mutation_type == MutationSelection.Flip:
            index = np.random.randint(0, len(kid.items))
            if kid.items[index].taken == 0:
                kid.items[index].taken = 1
            else:
                kid.items[index].taken = 0
            kid.compute_mass()
            kid.compute_value()
        elif mutation_type == MutationSelection.Swap:
            pass
    offspring = np.array(offspring)
    return np.concatenate((offspring, pops))


def new_generation(parents, offspring, max_values, max_mass):
    temp = list(np.concatenate((parents, offspring)))
    temp.sort(key=lambda x: x.value, reverse=True)
    generation = np.array(temp[0:pop_size])
    max_values.append(generation[0].value)
    max_mass.append(generation[0].mass)
    print(f"{generation[0].value}")
    np.random.shuffle(generation)
    return generation


def main():
    pops = populate(N, pop_size, max_weight, max_value, capacity)
    max_values = []
    max_mass = []
    for _ in range(epochs):
        parents = copy.deepcopy(pops)
        mutants = mutate(parents)
        pops = new_generation(parents, mutants, max_values, max_mass)

    plt.subplot(2,1,1)
    plt.plot([value for value in range(epochs)],[value for value in max_values])
    plt.ylabel("Values")
    plt.xlabel("Epoch")

    plt.subplot(2,1,2)
    plt.plot([value for value in range(epochs)],[value for value in max_mass])
    plt.ylabel("Mass")
    plt.xlabel("Epoch")

    plt.show()

if __name__ == "__main__":
    main()
    # test()