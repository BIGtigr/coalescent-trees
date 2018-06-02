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
    
    :param x: list -> DNA sequence of length, 'length'
    :param y: list -> DNA sequence of length, 'length'
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
    
    :param x: list -> DNA sequence of length, 'length'
    :param y: list -> DNA sequence of length, 'length'
    :return: fraction of differing sites between x and y
    """

    length = len(x)
    f_xy = min([num_differing_sites(x, y) / length, 0.75 - (1 / length)])
    return f_xy

def distance_xy(x, y):
    """ Calculates the distance between the sequences x and y
    
    :param x: list -> DNA sequence of length, 'length'
    :param y: list -> DNA sequence of length, 'length'
    :return: distance between x and y
    """

    d_xy = (-3 / 4) * math.log(1 - (4 * fraction_xy(x, y) / 3))
    return d_xy

def distance_matrix(node_set):
    """ Calculates the Jukes-Cantor distance matrix from a set of nodes

    :param node_set: set of node objects each with a sequence of length 'length'
    :return: Jukes-cantor distance matrix between the sequences of the set of nodes
    """

    matrix = {node_set[i].get_label():
                  {node_set[j].get_label():
                       distance_xy(list(node_set[i].get_sequence()), list(node_set[j].get_sequence()))
                   for j, node_y in enumerate(node_set)
                   }
              for i, node_x in enumerate(node_set)
              }
    return matrix

    # a = list(sequence_set[0])
    # b = list(sequence_set[4])
    # c = list(sequence_set[5])
    # test = distance_xy(list(sequence_set[0]), list(sequence_set[4]))
    # print(test)
    # print(a, '\n', b, '\n', c)
    # t1 = fraction_xy(a, b)
    # t2 = fraction_xy(a, c)
    # print(t1, t2)

def simulating_distance_matrix(tree):
    """ Calculates and returns the distance matrix for the leaves of a given tree.
    
    :param tree: a tree class object
    :return: matrix for the distances between each of the trees leaves.
    """

def pretty_print_dict(dict, decimals = 4):
    """ Prints a dictionary in a readable format
    
    SOURCE: https://stackoverflow.com/questions/14139258/how-to-make-a-nice-matrix-from-a-dictionary
    
    :param dict: dictionary object
    """
    layout = ":^10." + str(decimals) + "}"
    strs = " ".join("{"+"{0}{1}".format(i, layout) for i in range(len(dict.keys())+1))
    # print(strs)

    print(strs.format(" ", *dict))

    for key in dict:
        print(strs.format(key, *(float(dict[key].get(y, '-')) for y in dict)))

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

    ################ Calculating the distance matrix ##################

    # Generating a tree with 10 leaves (n=10) and 100 population size (pop_size=100)
    myKingman = Kingman()
    myTree = myKingman.simulate_one_tree(10, 100)

    # Generating a random sequence of length 50 and mutating down myTree
    rand_sequence = random_sequence(50)
    mutation_parameter = 0.0015
    mutate_tree(myTree.get_root(), rand_sequence, mu=mutation_parameter)

    # Finding the distance matrix from the set of leaf nodes
    myTree_leaves = myTree.get_leaves()
    matrix = distance_matrix(myTree_leaves)

    # Printing the matrix in a nice format (from a dictionary)
    print("Distances between the sequences of each pair of leaf nodes")
    pretty_print_dict(matrix)

    # Plotting the tree
    tree.plot_tree(myTree)



main()
