import tree
# from itertools import combinations
import math
import random as ra
import numpy as np

class Kingman:
    """ For all the operations to create a Kingman coalescent model
    """
    def __init__(self):
        self.available_nodes = []
        self.root_node = None

    def simulate_one_tree(self, n, pop_size):
        """ Simulates trees according to the Kingman coalescent model.
    
        inputs: number of available_nodes, n; effective population size, pop_size
        output: coalescent tree with n available_nodes.
        """

        import itertools as it
        from random import choice

        # each pair of lineages coalesces at rate 1/pop_size
        # given k lineages, total rate of coalescence is combination(k, 2)/pop_size

        k = n   # setting lineages to n
        t = 0

        # Initialising node labels, heights to zero, and matrix
        node_count = n
        self.available_nodes = [tree.Node(str(i)) for i in range(n)]
        for node in self.available_nodes:
            node.set_height(0)
        # matrix = {available_nodes[i]: {available_nodes[j]: matrix[i][j] for j in range(n)} for i in range(n)}

        while k > 1:
            # updating time, t
            rate = self.ncr(k, 2)/pop_size
            t_k = np.random.exponential(1/rate)
            t = t + t_k

            # new node m, with height t, and random children from available_nodes and popping them
            m = tree.Node(str(node_count))
            node_count += 1
            m.set_height(t)

            # Gets the combinations of 2 different nodes and their indices (pairs) from the available_nodes
            # Then setting into a list
            pairs = it.combinations(enumerate(self.available_nodes), 2)
            pairs = [(i[0], i[1]) for i in pairs]
            # At this point each node in a pair is a tuple -> (available_nodes index, node object)

            # Selecting a random pair (by index) and setting as children of m
            # Note: index [0] is the index from available nodes | [1] is the node object
            pairs_index = choice(range(len(pairs)))
            left_child = pairs[pairs_index][0]
            right_child = pairs[pairs_index][1]
            m.add_child(left_child[1])
            m.add_child(right_child[1])

            # Removing added children from list of available_nodes
            # Popping right child first to maintain index integrity of available_nodes
            index_to_pop = right_child[0]
            self.available_nodes.pop(index_to_pop)
            index_to_pop = left_child[0]
            self.available_nodes.pop(index_to_pop)

            # adding m to set of available_nodes
            self.available_nodes.append(m)

            # one less lineage
            k -= 1

            # ----- End of While Loop -----

        self.root_node = m
        return self.root_node.get_height()

    def simulate_trees(self, number_of_sims):
        """ Simulates a tree ~number_of_sims~ times.
        :param number_of_sims: number of simulations (int)
        :return:  mean height of all simluated trees
        """

        sum = 0
        for i in range(number_of_sims):
            sum += self.simulate_one_tree(10, 100)

        mean = sum/number_of_sims

        return mean

    @staticmethod
    def ncr(n, r):
        """ nCr caclculation. n choose r. combinations with repetition

        :param n: number of options
        :param r: number selected from n
        :return: number of combinations with repetition
        """
        f = math.factorial
        return f(n) // (f(r) * f(n - r))


def main():
    kingman = Kingman()
    kingman.simulate_one_tree(10, 100)

    theoretical_mean = 2*100*(1 - (1/10))
    print(theoretical_mean)

    mean = kingman.simulate_trees(1000)
    print(mean)

    my_tree = tree.Tree(kingman.root_node)
    tree.plot_tree(my_tree)



main()