import random as ra

def random_sequence(length):
    """ Generates a random sequence of DNA bases of a given length
    
    :param length: length of sequence to be generated
    :return: random sequence of length 'length'
    """

    bases = 'ACTG'
    sequence = ""
    for i in range(length):
        sequence += ra.choice(bases)

    return sequence

seq = random_sequence(5)
print(seq)
