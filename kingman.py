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

        # each pair of lineages coalesces at rate 1/pop_size
        # given k lineages, total rate of coalescence is combination(k, 2)/pop_size

        k = n   # setting lineages to n
        t = 0

        # Initialising node labels, heights to zero, and matrix
        node_count = n
        self.available_nodes = [tree.Node(str(i + 1)) for i in range(n)]
        for node in self.available_nodes:
            node.set_height(0)
        # matrix = {available_nodes[i]: {available_nodes[j]: matrix[i][j] for j in range(n)} for i in range(n)}

        while k > 1:
            # updating time, t
            rate = self.ncr(k, 2)/pop_size
            t_k = np.random.exponential(1/rate)
            t = t + t_k

            # new node m, with height t, and random children from available_nodes and popping them
            m = tree.Node(str(n))
            node_count += 1
            m.set_height(t)
            m_num_children = 2
            node_count += 1

            yo = it.combinations(self.available_nodes, 2)
            for i in yo:
                print(i[0].get_label(), i[1].get_label())
            print('done')

            # for i in range(m_num_children):
            #     m.add_child(self.available_nodes.pop(ra.randint(0, len(self.available_nodes)-1)))



            # print("m's children are:")
            # for i in m.get_children():
            #     print(i.get_label())
            # print()

            # print("leftover available_nodes:")
            # for i in self.available_nodes:
            #     print(i.get_label())
            # print()

            # adding m to set of available_nodes
            # self.available_nodes.append(m)


            # one less lineage
            k -= 1
            # print("New loop --------")

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

        print(sum)
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
    # my_tree = tree.Tree(kingman.root_node)
    # tree.plot_tree(my_tree)
    #
    # theoretical_mean = 2*100*(1 - (1/10))
    # print(theoretical_mean)
    #
    #
    # mean = kingman.simulate_trees(1000)
    # print(mean)



main()