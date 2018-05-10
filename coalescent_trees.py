def simulate_trees(n, pop_size):
    """ Simulates trees according to the Kingman coalescent model.

    inputs: number of leaves, n; effective population size, pop_size
    output: coalescent tree with n leaves.
    """

    # each pair of lineages coalesces at rate 1/pop_size
    # given k lineages, total rate of coalescence is combination(k, 2)/pop_size

    for i in range(n):
        leaves[i] =