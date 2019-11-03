# 0-1 knapsack problem using genetic algorithm
# with (mu + lambda) evolution strategy
# http://www.scholarpedia.org/article/Evolution_strategies
# https://www.tutorialspoint.com/genetic_algorithms/index.htm

import matplotlib.pyplot as plt
import numpy as np
from Knapsack import Knapsack
from Enums import ParentSelection, MutationSelection

# Config
N = 100  # Number of items [100, 250, 500]
capacity = N * 3
max_value = 20
max_weight = 10

pop_size = 50  # mu
epochs = 200
num_offspring = 20  # lambda
num_breeding_parents = 40  # p
mutation_chance = 0.4  # Chance of mutation to occur

parent_selection_method = ParentSelection.Tournament
mutation_type = MutationSelection.Flip
# End of config


def populate(num_genes, pop_size, max_weight, max_value, capacity):
    return np.array([Knapsack(num_genes, max_weight, max_value, capacity) for _ in range(pop_size)])


def compute_fitness(pops):
    fitness = []
    for pop in pops:
        pop.compute_mass()
        fitness.append(pop.compute_value())
    return fitness


def selection(pops, fitness, num_breeding_parents, parent_selection):
    parents = []
    if parent_selection == ParentSelection.Random:
        indexes = list(range(pops.shape[0]))
        for _ in range(num_breeding_parents):
            idx = indexes.pop(np.random.randint(len(indexes)))
            parents.append(pops[idx])
    elif parent_selection == ParentSelection.Tournament:
        for _ in range(num_breeding_parents):
            parent1 = pops[np.random.randint(0, pops.shape[0])]
            parent2 = pops[np.random.randint(0, pops.shape[0])]
            if parent1.items[0].value >= parent2.items[0].value:
                parents.append(parent1)
            else:
                parents.append(parent2)
    elif parent_selection == ParentSelection.Fittest:
        for _ in range(num_breeding_parents):
            parents.append(pops[fitness.index(max(fitness))])
    return parents


def crossover(parents, num_offspring, num_items):
    # One point crossover
    offspring = []
    for _ in range(num_offspring):
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


def new_generation(pops, offspring):
    temp = list(np.concatenate((pops, offspring)))
    temp.sort(key=lambda x: x.value, reverse=True)
    generation = np.array(temp[0:50])
    print(f"{generation[0].value}")
    np.random.shuffle(generation)
    return generation


pops = populate(N, pop_size, max_weight, max_value, capacity)

for epoch in range(epochs):
    fitness = compute_fitness(pops)
    parents = selection(pops, fitness, num_breeding_parents, parent_selection_method)
    offspring = crossover(parents, num_offspring, N)
    mutants = mutate(offspring, mutation_chance, mutation_type)
    pops = new_generation(pops, mutants)
    # for i in range(pop_size):
    #     plt.scatter(pops[i].value, pops[i].mass)
    # plt.savefig(f'fig_{epoch}.png')
    # plt.show()
    # plt.clf()
