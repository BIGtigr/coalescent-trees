import tree
# from itertools import combinations
import math
import random as ra

class Kingman:
    """ For all the operations to create a Kingman coalescent model
    """
    def __init__(self):
        self.leaves = []
        self.root_node = None

    def simulate_trees(self, n, pop_size):
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

        while k > 2:
            # updating time, t
            # Wrap this around an exponential distribution (Random number generator!)
            t_k = 1/(self.ncr(k, 2)/pop_size)
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
            self.root_node = m

            # one less lineage
            k -= 1
            # print("New loop --------")


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
    kingman.simulate_trees(10, 100)
    print(kingman.root_node.get_label())
    #
    print(kingman.root_node.get_height())
    tm = 2*100*(1 - (1/10))
    print(tm)

    # x = ra.randint(0, 4)
    # print(x)
    my_tree = tree.Tree(kingman.root_node)
    tree.plot_tree(my_tree)

main()