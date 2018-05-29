import random as ra
import math
import numpy as np
from kingman import Kingman
import tree

def random_sequence(length):
    """ Generates a random sequence of DNA bases of a given length
    
    :param length: length of sequence to be generated
    :return: random sequence of length 'length'
    """

    bases = 'ACTG'
    sequence = []
    for i in range(length):
        sequence += ra.choice(bases)

    return sequence

def mutate(sequence, time, mu):
    """ Mutates a given sequence according to the Jukes-Cantor model of mutation
    
    :param sequence: some DNA sequence as a string
    :param time: time as a float
    :param mu: mutation rate
    :return: 
    """

    length = len(sequence)

    # Calculating the number of mutaitons according to a poisson distribution with total rate length*time*mu
    numMutation = np.random.poisson(length*time*mu)

    print(f"Number of mutations: {numMutation}")
    print(f"Original Sequence = {sequence}")

    # For each mutation, choose a site and mutate it
    bases = 'ACTG'
    for i in range(numMutation):
        # Choosing a site
        site = math.floor(np.random.random() * length)
        sequence[site] = ra.choice(bases)

    print(f"Mutated Sequence = {sequence}")
    return sequence

def foo(node, sequence, time=1, mu=0.3):
    if node.is_root() == False:
        sequence = mutate(sequence, time, mu)
    node.set_sequence(sequence)

    if node.is_leaf == True:
        return
    else:
        foo(node.get_children()[0], sequence)     # get LEFT child
        foo(node.get_children()[1], sequence)     # get RIGHT child


def ncr(n, r):
    """ nCr caclculation. n choose r. combinations with repetition

    :param n: number of options
    :param r: number selected from n
    :return: number of combinations with repetition
    """
    f = math.factorial
    return f(n) // (f(r) * f(n - r))

def main():
    seq = random_sequence(5)
    # print(seq)
    sequence = ['A', 'T', 'C', 'G']
    time = 1
    mu = 0.3

    mutate(sequence, time, mu)


    myKingman = Kingman()
    myTree = myKingman.simulate_one_tree(4, 100)

    myTree.get_root().set_sequence(sequence)
    print(f"The root has sequence = {myTree.get_root().get_sequence()}")
    tree.plot_tree(myTree)

    foo(myTree.get_root(), seq)






main()
