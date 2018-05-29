import tree
# from itertools import combinations
import math
import random as ra
import numpy as np

class Kingman:
    """ For all the operations to create a Kingman coalescent model
    """
    def __init__(self):
        self.leaves = []
        self.root_node = None

    def simulate_one_tree(self, n, pop_size):
        """ Simulates trees according to the Kingman coalescent model.
    
        inputs: number of leaves, n; effective population size, pop_size
        output: coalescent tree with n leaves.
        """

        # each pair of lineages coalesces at rate 1/pop_size
        # given k lineages, total rate of coalescence is combination(k, 2)/pop_size

        k = n   # setting lineages to n
        t = 0

        node_count = n
        for i in range(node_count):
            self.leaves.append(tree.Node(f'leaf {i}'))


        while k > 1:
            # updating time, t
            # Wrap this around an exponential distribution (Random number generator!)
            rate = self.ncr(k, 2)/pop_size
            # print(rate)
            t_k = np.random.exponential(1/rate)
            t = t + t_k

            # new node m, with height t, and random children from available leaves and popping them
            m = tree.Node(f'leaf {node_count}')
            m.set_height(t)
            m_num_children = 2
            node_count += 1
            # print(f"new {m.get_label()}")

            for i in range(m_num_children):
                m.add_child(self.leaves.pop(ra.randint(0, len(self.leaves)-1)))

            # print("m's children are:")
            # for i in m.get_children():
            #     print(i.get_label())
            # print()

            # print("leftover leaves:")
            # for i in self.leaves:
            #     print(i.get_label())
            # print()

            # adding m to set of available nodes
            self.leaves.append(m)


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
    my_tree = tree.Tree(kingman.root_node)
    tree.plot_tree(my_tree)

    theoretical_mean = 2*100*(1 - (1/10))
    print(theoretical_mean)


    mean = kingman.simulate_trees(1000)
    print(mean)



main()