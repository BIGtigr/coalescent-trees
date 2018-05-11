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

        for i in self.leaves:
            print(i.get_label())

        while k > 2:
            t_k = math.exp(self.ncr(k, 2)/pop_size)
            t = t + t_k

            print(t)

            # new node m, with height t, and random children from available leaves.
            m = Node()
            m.set_height(t)

            leaf_indices = ra.sample([i for i in range(len(self.leaves))],
                                     2)
            for i in leaf_indices:
                # m.add_child(leaf_indices)
                m.add_child(self.leaves.pop(i))

            for i in m.get_leaves():
                print(i.get_label())
            # for i in children:
            #     print(i.get_label())

            print(self.leaves)


            # print(t_k)
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
    kingman.simulate_trees(3, 10)
    # x = ra.randint(0, 4)
    # print(x)

main()