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
NUMBER_OF_ITEMS = 500  # Number of items [100, 250, 500]
CAPACITY = NUMBER_OF_ITEMS * 3
MAX_VALUE = 20
MAX_WEIGHT = 10

POP_SIZE = 20  # MU
EPOCHS = 50
NUM_OFFSPRING = 20  # LAMBDA
NUM_BREEDING_PARENTS = 2 * NUM_OFFSPRING  # P
NUM_TO_MUTATE = 6 * POP_SIZE  # LAMBDA
MUTATION_CHANCE = 0.4  # CHANCE OF MUTATION TO OCCUR

MUTATION_TYPE = MutationSelection.Flip
PARENT_SELECTION = ParentSelection.Random


# End of config


def populate(num_genes, pop_size, max_weight, max_value, capacity):
    return np.array([Knapsack(num_genes, max_weight, max_value, capacity) for _ in range(pop_size)])


def compute_fitness(pops):
    fitness = []
    for pop in pops:
        pop.compute_mass()
        fitness.append(pop.compute_value())
    return fitness


def random_selection(pops, num_breeding_parents, parent_selection):
    parents = []
    if parent_selection == ParentSelection.Random:
        for _ in range(num_breeding_parents):
            idx = np.random.randint(0, len(pops))
            parents.append(pops[idx])
    return parents


def uniform_crossover(parents, num_offspring, num_items):
    offspring = []
    crossover_vector = [np.random.randint(0, 2) for _ in range(num_items)]  # choose 0 or 1
    for _ in range(num_offspring):
        parentA = parents.pop().items
        parentB = parents.pop().items
        kid = [parentA[idx] if crossover_vector[idx] else parentB[idx] for idx in range(len(crossover_vector))]
        temp = Knapsack(NUMBER_OF_ITEMS, MAX_WEIGHT, MAX_VALUE, CAPACITY)
        temp.items = np.array(kid)
        temp.compute_mass()
        temp.compute_value()
        offspring.append(temp)
    return np.array(offspring)


def mutate(pops, num_to_mutate):
    offspring = []
    for _ in range(num_to_mutate):
        offspring.append(copy.copy(pops[np.random.randint(0, len(pops))]))
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


def new_generation(parents, offspring, max_values, max_mass,average_value,average_mass):
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
    pops = populate(NUMBER_OF_ITEMS, POP_SIZE, MAX_WEIGHT, MAX_VALUE, CAPACITY)
    max_values = []
    max_mass = []
    average_value = []
    average_mass = []
    for _ in range(EPOCHS):
        old_generation = copy.deepcopy(pops)
        parents = random_selection(old_generation, NUM_BREEDING_PARENTS, PARENT_SELECTION)
        offspring = uniform_crossover(parents, NUM_OFFSPRING, NUMBER_OF_ITEMS)
        mutants = mutate(offspring, NUM_TO_MUTATE)
        pops = new_generation(old_generation, mutants, max_values, max_mass,average_value,average_mass)

    return pops, max_values, max_mass, average_value, average_mass

def show_results(max_values,max_mass,average_value,average_mass):
    plt.style.use('ggplot')
    plt.subplot(2, 1, 1)
    plt.title("Strategia ewolucyjna z wybraniem rodzica")
    plt.plot([value for value in range(EPOCHS)], [value for value in max_values])
    plt.plot([value for value in range(EPOCHS)], [value for value in average_value], '--')
    plt.ylabel("Values")
    plt.xlabel("Epoch")
    plt.legend(["Wartość przystosowania najlepszych osobników.", "Wartość średniego przystosowania"])


    plt.subplot(2, 1, 2)
    plt.plot([value for value in range(EPOCHS)], [value for value in max_mass])
    plt.plot([value for value in range(EPOCHS)], [value for value in average_mass],'--')
    plt.ylabel("Mass")
    plt.xlabel("Epoch")
    plt.legend(["Wartość przystosowania najlepszych osobników.", "Wartość średniego przystosowania"])

    plt.show()


def main():
    _, max_values, max_mass,average_value,average_mass = realize_algorithm()
    show_results(max_values,max_mass,average_value,average_mass)


if __name__ == "__main__":
    main()
    # test()
