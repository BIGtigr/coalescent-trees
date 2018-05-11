from tree import Node
# from itertools import combinations
import math

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

        leaves = []
        for i in range(n):
            leaves.append(Node(f'leaf {i}'))

        for i in leaves:
            print(i.get_label())

        while k > 1:
            t_k = math.exp(self.ncr(k, 2)/pop_size)
            t = t + t_k

            m = Node()

            print(t_k)
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


main()