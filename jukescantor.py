import random as ra
import math
import numpy as np
from tree import plot_tree, compute_upgma_tree
from kingman import simulate_one_tree

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

    # Calculating the number of mutations according to a poisson distribution with total rate length*time*mu
    numMutation = np.random.poisson(length * time * mu)

    # For each mutation, choose a site and mutate it
    bases = 'ACTG'
    for i in range(numMutation):
        # Choosing a site
        site = math.floor(np.random.random() * length)
        sequence[site] = ra.choice(bases)

    return sequence

def mutate_tree(node, sequence, mu=0.0015):
    """ Recursively mutates down the branches of a tree at node
    
    :param node: Node to mutate and recursively mutate it's children
    :param sequence: the sequence of that parent node
    :param time: default value of 1
    :param mu: default value of 0.3
    :return: None. Just manipulates the self.sequence of a node
    """

    if node.is_root() == False:
        branch_length = node.get_parent().get_height() - node.get_height()
        sequence = mutate(sequence, branch_length, mu)
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

def distance_matrix_dict(node_set):
    """ Calculates the Jukes-Cantor distance matrix from a set of nodes

    :param node_set: set of node objects each with a sequence of length 'length'
    :return: dictionary -> Jukes-cantor distance matrix between the sequences of the set of nodes
    """

    matrix = {node_set[i].get_label():
                  {node_set[j].get_label():
                       distance_xy(list(node_set[i].get_sequence()), list(node_set[j].get_sequence()))
                   for j, node_y in enumerate(node_set)
                   }
              for i, node_x in enumerate(node_set)
              }

    return matrix

def distance_matrix(node_set):
    """ Calculates the Jukes-Cantor distance matrix from a set of nodes

    :param node_set: set of node objects each with a sequence of length 'length'
    :return: 2d array -> Jukes-cantor distance matrix between the sequences of the set of nodes
    """

    matrix = [
        [distance_xy(node_x.get_sequence(), node_y.get_sequence()) for node_y in node_set]
        for node_x in node_set
    ]
    matrix = np.array(matrix)

    return matrix

def get_leaves_in_order(leaf_nodes):
    """ Sorts a list of leaf nodes in order according to their labels
    
    :param leaf_nodes: List of unsorted leaf nodes.
    :return: list of sorted leaf nodes according to their labels
    """

    sorted_leaf_nodes = [None] * len(leaf_nodes)

    for leaf in leaf_nodes:
        index = int(leaf.get_label())
        sorted_leaf_nodes[index] = leaf

    return sorted_leaf_nodes

def simulate_distance_matrix(tree):
    """ Calculates and returns the distance matrix for the leaves of a given tree.
    
    :param tree: a tree class object
    :return: matrix for the distances between each of the trees leaves.
    """

    leaves = tree.get_leaves()
    sorted_leaves = get_leaves_in_order(leaves)
    matrix = distance_matrix(sorted_leaves)
    return matrix

def display_distance_matrix(matrix, round_to=4, col_width=9):
    """ Displays a distance matrix in an easy to read fashion
    
    :param matrix: numpy.array of a distance matrix
    """

    size = len(matrix)
    layout = ":^" + str(col_width) + "}"
    scaffold = " ".join("{"+"{0}{1}".format(leaf_num, layout) for leaf_num in range(size+1))

    print(scaffold.format(" ", *(i for i in range(size+1))))

    for i in range(size):
        print(scaffold.format(i, *(round(matrix[i][j], round_to) if matrix[i][j] != 0 else '-' for j in range(size))))

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

def simulate_and_reconstruct(tree, sequence_length, mutation_parameter, display=True):
    """ Simulates a tree with a sequence of length 'sequence_length' and reconstructs it.
    
    Reconstruction is done by creating a Jukes Cantor distance matrix then converting it into a UPGMA
    tree. The distance matrix and resulting UPGMA tree is then displayed
    
    :param tree: tree -> tree to be simulated with a sequence
    :param sequence_length: int -> DNA sequence length to create sequence for simulation 
    :param mutation_parameter: float -> the rate of mutation
    :return: Displayed distance matrix and plotted reconstructed UPGMA tree
    """

    # Mutating sequence down tree
    sequence = random_sequence(sequence_length)
    mutate_tree(tree.get_root(), sequence, mu=mutation_parameter)

    # Creating distance matrix
    matrix = simulate_distance_matrix(tree)
    if display:
        print(f"~~~~~~~~~~ Distance matrix (L = {sequence_length}) ~~~~~~~~~~")
        print("(Note: Rows and cols correspond to labelled leaf nodes)")
        display_distance_matrix(matrix)

    # Reconstructing and plotting
    reconstructed_tree = compute_upgma_tree(matrix)
    if display:
        print(f"~~~~~~~~~~ UPGMA Tree (L = {sequence_length}) ~~~~~~~~~~\n")
        plot_tree(reconstructed_tree)
    return reconstructed_tree

def ncr(n, r):
    """ nCr caclculation. n choose r. combinations with repetition

    :param n: number of options
    :param r: number selected from n
    :return: number of combinations with repetition
    """
    f = math.factorial
    return f(n) // (f(r) * f(n - r))

def main():
    """
    myTree = simulate_one_tree(4, 100)
    plot_tree(myTree)

    rand_sequence = random_sequence(5)
    mutate_tree(myTree.get_root(), rand_sequence)
    """

    ################ Calculating the distance matrix ##################

    """
    # Generating a tree with 10 leaves (n=10) and 100 population size (pop_size=100)
    myTree = simulate_one_tree(10, 100)

    # Generating a random sequence of length 50 and mutating down myTree
    sequence_length = 50
    rand_sequence = random_sequence(sequence_length)
    mutation_parameter = 0.0015
    mutate_tree(myTree.get_root(), rand_sequence, mu=mutation_parameter)

    # Finding the distance matrix from the set of leaf nodes
    matrix = simulate_distance_matrix(myTree)
    display_distance_matrix(matrix)

    # Plotting the tree
    plot_tree(myTree)
    """

    ################ Simulating trees with different sequence lengths ##################

    # Generating a tree with 10 leaves (n=10) and 100 population size (pop_size=100)
    myTree = simulate_one_tree(10, 100)
    print("~~~~~~~~~~ Original Tree ~~~~~~~~~~")
    plot_tree(myTree)

    # Simulating and reconstructing trees with sequence lengths 50, 200, and 1000
    mutation_parameter = 0.0015
    simulate_and_reconstruct(myTree, 50, mutation_parameter)
    simulate_and_reconstruct(myTree, 200, mutation_parameter)
    simulate_and_reconstruct(myTree, 1000, mutation_parameter)

    print("As the sequence length increases, the tree reconstructions resemble the original tree more and more.")

# main()
