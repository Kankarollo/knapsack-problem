# 0-1 knapsack problem using genetic algorithm
# with (mu + lambda) evolution strategy
# http://www.scholarpedia.org/article/Evolution_strategies
# https://www.tutorialspoint.com/genetic_algorithms/index.htm

import seaborn as sns
import numpy as np
from Knapsack import Knapsack
from Enums import ParentSelection, MutationSelection

# Config
N = 100  # Number of items [100, 250, 500]
capacity = N * 5
max_value = 20
max_weight = 10

pop_size = 50  # mu
epochs = 20
num_offspring = 20  # lambda
num_breeding_parents = 40  # p
mutation_chance = 0.8  # Chance of mutation to occur

parent_selection_method = ParentSelection.Random
mutation_type = MutationSelection.Flip
# End of config


def populate(num_genes, pop_size, max_weight, max_value, capacity):
    return np.array([Knapsack(num_genes, max_weight, max_value, capacity) for _ in range(pop_size)])


def compute_fitness(pops):
    for pop in pops:
        pop.compute_mass()
        pop.compute_value()


def create_offspring(pops, num_breeding_parents, num_offspring, parent_selection, num_items):
    parents = []
    if parent_selection == ParentSelection.Random:
        indexes = list(range(pops.shape[0]))
        for i in range(num_breeding_parents):
            idx = indexes.pop(np.random.randint(len(indexes)))
            parents.append(pops[idx])
    elif parent_selection == ParentSelection.Tournament:
        pass

    # One point crossover
    offspring = []
    for i in range(num_offspring):
        first_half = parents.pop().items[0:int(num_items/2)]
        second_half = parents.pop().items[int(num_items/2):]
        temp = Knapsack(N, max_weight, max_value, capacity)
        temp.items = np.concatenate((first_half, second_half))
        temp.compute_mass()
        temp.compute_value()
        offspring.append(temp)
    return np.array(offspring)


def mutate(offspring, mutation_chance, mutation_type):
    for kid in offspring:
        if np.random.rand() < mutation_chance:
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
    return offspring


def select_new_generation(pops, offspring):
    temp = list(np.concatenate((pops, offspring)))
    temp.sort(key=lambda x: x.value, reverse=True)
    new_generation = np.array(temp[0:50])
    print(f"{new_generation[0].value}")
    np.random.shuffle(new_generation)
    return new_generation


pops = populate(N, pop_size, max_weight, max_value, capacity)

for epoch in range(epochs):
    compute_fitness(pops)
    offspring = create_offspring(pops, num_breeding_parents, num_offspring, parent_selection_method, N)
    offspring = mutate(offspring, mutation_chance, mutation_type)
    pops = select_new_generation(pops, offspring)
