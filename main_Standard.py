# 0-1 knapsack problem using genetic algorithm
# with (mu + lambda) evolution strategy
# http://www.scholarpedia.org/article/Evolution_strategies
# https://www.tutorialspoint.com/genetic_algorithms/index.htm
# Dodac crossover jednorodne (losowy wektor gdzie zachodzi wymiana)
# mutacja flip, male prawdopodobienstwo
# selekcja losowa

import matplotlib.pyplot as plt
import numpy as np
import copy
from Knapsack import Knapsack
from Enums import ParentSelection, MutationSelection

# Config
N = 250  # NUMBER OF ITEMS [100, 250, 500]
CAPACITY = N * 3
MAX_VALUE = 20
MAX_WEIGHT = 10

POP_SIZE = 20  # MU
EPOCHS = 20
NUM_OFFSPRING = 6*POP_SIZE  # LAMBDA
MUTATION_CHANCE = 0.4  # CHANCE OF MUTATION TO OCCUR

MUTATION_TYPE = MutationSelection.Flip
# End of config


def populate(num_genes, pop_size, max_weight, max_value, capacity):
    return np.array([Knapsack(num_genes, max_weight, max_value, capacity) for _ in range(pop_size)])


def mutate(pops):
    offspring = []
    for _ in range(NUM_OFFSPRING):
        offspring.append(copy.copy(pops[np.random.randint(0,len(pops))]))
    for kid in offspring:
        if np.random.rand() < MUTATION_CHANCE:
            if MUTATION_TYPE == MutationSelection.Flip:
                index = np.random.randint(0, len(kid.items))
                if kid.items[index].taken == 0:
                    kid.items[index].taken = 1
                else:
                    kid.items[index].taken = 0
                kid.compute_mass()
                kid.compute_value()
            elif MUTATION_TYPE == MutationSelection.Swap:
                pass
    offspring = np.array(offspring)
    return np.concatenate((offspring, pops))


def new_generation(parents, offspring, max_values, max_mass, average_value,average_mass):
    temp = list(np.concatenate((parents, offspring)))
    temp.sort(key=lambda x: x.value, reverse=True)
    generation = np.array(temp[0:POP_SIZE])
    max_values.append(generation[0].value)
    max_mass.append(generation[0].mass)
    calculate_average_value(average_value,average_mass,generation)
    print(f"{generation[0].value}")
    np.random.shuffle(generation)
    return generation

def calculate_average_value(average_value, average_mass, generation):
    sum_value = 0.0
    sum_mass = 0.0
    for index, element in enumerate(generation):
        sum_value += element.value
        sum_mass += element.mass
    average_value.append(sum_value/(index + 1))
    average_mass.append(sum_mass/(index + 1))

def realize_algorithm():
    pops = populate(N, POP_SIZE, MAX_WEIGHT, MAX_VALUE, CAPACITY)
    max_values = []
    max_mass = []
    average_value = []
    average_mass = []
    for _ in range(EPOCHS):
        parents = copy.deepcopy(pops)
        mutants = mutate(parents)
        pops = new_generation(parents, mutants, max_values, max_mass, average_value, average_mass)
    return pops,max_values,max_mass,average_value,average_mass


def show_results(max_values, max_mass, average_value,average_mass):
    plt.style.use('ggplot')
    plt.subplot(2, 1, 1)
    plt.title("Strategia ewolucyjna")
    plt.plot([value for value in range(EPOCHS)], [value for value in max_values])
    plt.plot([value for value in range(EPOCHS)], [value for value in average_value])
    plt.ylabel("Values")
    plt.xlabel("Epoch")
    plt.legend(["Wartość przystosowania najlepszych osobników.", "Wartość średniego przystosowania"])

    plt.subplot(2, 1, 2)
    plt.plot([value for value in range(EPOCHS)], [value for value in max_mass])
    plt.plot([value for value in range(EPOCHS)], [value for value in average_mass])
    plt.ylabel("Mass")
    plt.xlabel("Epoch")
    plt.legend(["Wartość przystosowania najlepszych osobników.", "Wartość średniego przystosowania"])

    plt.show()

def main():
    _, max_values, max_mass, average_value,average_mass = realize_algorithm()
    show_results(max_values,max_mass,average_value,average_mass)

if __name__ == "__main__":
    main()
