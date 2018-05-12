from tree import Node
# from itertools import combinations
import math
import random as ra

class Kingman:
    """ For all the operations to create a Kingman coalescent model
    """
    def __init__(self):
        self.leaves = []

    def simulate_trees(self, n, pop_size):
        """ Simulates trees according to the Kingman coalescent model.
    
        inputs: number of leaves, n; effective population size, pop_size
        output: coalescent tree with n leaves.
        """

        # each pair of lineages coalesces at rate 1/pop_size
        # given k lineages, total rate of coalescence is combination(k, 2)/pop_size

        k = n   # setting lineages to n
        t = 0

        for i in range(n):
            self.leaves.append(Node(f'leaf {i}'))

        while k > 2:
            # updating time, t
            t_k = math.exp(self.ncr(k, 2)/pop_size)
            t = t + t_k

            # new node m, with height t, and random children from available leaves and popping them
            m = Node()
            m.set_height(t)
            m_num_children = 2

            for i in range(m_num_children):
                m.add_child(self.leaves.pop(ra.randint(0, len(self.leaves)-1)))

            print("m's children are:")
            for i in m.get_leaves():
                print(i.get_label())
            print()

            print("leftover leaves:")
            for i in self.leaves:
                print(i.get_label())
            print()

            # adding m to set of available nodes
            self.leaves.append(m)

            # one less lineage
            k -= 1

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
    kingman.simulate_trees(5, 10)
    # x = ra.randint(0, 4)
    # print(x)

main()