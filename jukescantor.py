import random as ra
import math
import numpy as np
import tree
from kingman import Kingman


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
    numMutation = np.random.poisson(length * time * mu)

    # For each mutation, choose a site and mutate it
    bases = 'ACTG'
    for i in range(numMutation):
        # Choosing a site
        site = math.floor(np.random.random() * length)
        sequence[site] = ra.choice(bases)

    return sequence


def mutate_tree(node, sequence, time=1, mu=0.3):
    """ Recursively mutates down the branches of a tree at node
    
    :param node: Node to mutate and recursively mutate it's children
    :param sequence: the sequence of that parent node
    :param time: default value of 1
    :param mu: default value of 0.3
    :return: None. Just manipulates the self.sequence of a node
    """

    if node.is_root() == False:
        sequence = mutate(sequence, time, mu)
    node.set_sequence(sequence)

    if node.is_leaf() == True:
        return
    else:
        mutate_tree(node.get_children()[0], list(sequence))  # get LEFT child
        mutate_tree(node.get_children()[1], list(sequence))  # get RIGHT child


def num_differing_sites(x, y):
    """ Calculates the number of differing sites between two sequences of the same length
    
    :param x: DNA sequence of length, 'length'
    :param y: DNA sequence of length, 'length'
    :return: number of differing sites between x and y
    """

    # Note: if extending this method for sequences of different length
    #       use try statements

    count = 0
    for i, base in enumerate(x):
        if x[i] != y[i]:
            count += 1
    return count

def fraction_xy(x, y):
    """ Returns the fraction of differing sites between two sequences x and y (equal length)
    
    :param x: DNA sequence of length, 'length'
    :param y: DNA sequence of length, 'length'
    :return: fraction of differing sites between x and y
    """

    length = len(x)
    f_xy = min([num_differing_sites(x, y) / length, 0.75 - (1 / length)])
    return f_xy

def distance_xy(x, y):
    """ Calculates the distance between the sequences x and y
    
    :param x: DNA sequence of length, 'length'
    :param y: DNA sequence of length, 'length'
    :return: distance between x and y
    """

    d_xy = (-3 / 4) * math.log(1 - (4 * fraction_xy(x, y) / 3))
    return d_xy

def distance_matrix(x, y):
    """ Calculates the Jukes-Cantor distance matrix from a set of sequences
    
    :param x: DNA sequence of length, 'length'
    :param y: DNA sequence of length, 'length'
    :return: Jukes-cantor distance matrix between sequences x and y
    """

    # Creating the matrix
    # matrix = {nodes[i]: {nodes[j]: matrix[i][j] for j in range(n)} for i in range(n)}

    # Distance between sequences x and y
    # d_xy = distance_xy()

    yo = distance_xy(x, y)
    print(yo)



def ncr(n, r):
    """ nCr caclculation. n choose r. combinations with repetition

    :param n: number of options
    :param r: number selected from n
    :return: number of combinations with repetition
    """
    f = math.factorial
    return f(n) // (f(r) * f(n - r))


def main():
    # myKingman = Kingman()
    # myTree = myKingman.simulate_one_tree(4, 100)
    # tree.plot_tree(myTree)
    #
    # rand_sequence = random_sequence(5)
    # mutate_tree(myTree.get_root(), rand_sequence)

    seq1 = list("ACTG")
    seq2 = list("ACTT")
    seq3 = list("ACTA")
    seq4 = list("CCTG")
    seq5 = list("CCCC")
    seq6 = list("GCGG")
    sequence_set = [seq1, seq2, seq3, seq4, seq5, seq6]
    print(sequence_set)

    distance_matrix(seq1, seq2)

main()
