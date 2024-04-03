import numpy as np
from HebbianNetwork import HebbianNetwork

if __name__ == "__main__":
    # Create a network with 30 inputs and 3 outputs
    network = HebbianNetwork.from_file('network.npy')

    input = np.zeros(10)

    location = 9
    height = 3

    input[location] = height
    print(input)
    print(network.predict(input))