# Imports here
from tree import plot_tree
from kingman import simulate_one_tree
from jukescantor import simulate_and_reconstruct

def mcmc():
    pass

def main():
    my_tree = simulate_one_tree(10, 100)
    plot_tree(my_tree)
    new_tree = simulate_and_reconstruct(my_tree, 1000, 0.0015, display=False)
    plot_tree(new_tree)

main()