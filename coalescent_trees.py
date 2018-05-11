from tree import Node
# from itertools import combinations
import math

def nCr(n, r):
    f = math.factorial
    return f(n) // (f(r) * f(n-r))

def simulate_trees(n, pop_size):
    """ Simulates trees according to the Kingman coalescent model.

    inputs: number of leaves, n; effective population size, pop_size
    output: coalescent tree with n leaves.
    """

    # each pair of lineages coalesces at rate 1/pop_size
    # given k lineages, total rate of coalescence is combination(k, 2)/pop_size

    k = n   # setting lineages to n
    t = 0

    leaves = []
    for i in range(n):
        leaves.append(Node(f'leaf {i}'))

    for i in leaves:
        print(i.get_label())

    # while k > 1:


def main():
    simulate_trees(3, 10)

main()