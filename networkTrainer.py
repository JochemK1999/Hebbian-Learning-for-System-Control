import numpy as np
import pandas as pd

from HebbianNetwork import HebbianNetwork

if __name__ == "__main__":
    df = pd.read_csv('data.csv')

    # Extract inputs (first 10 columns) and outputs (last column) as NumPy arrays
    inputs = df.iloc[:, :-1].values  # Extract all rows and all but the last column
    outputs = df.iloc[:, -1].values  # Extract all rows and the last column

    filtered_inputs = []
    filtered_outputs = []
    for input, output in zip(inputs, outputs):
        if(sum(input) > 0):
            filtered_inputs.append(input)
            filtered_outputs.append(output)

    # Create a network with 30 inputs and 3 outputs
    network = HebbianNetwork.from_dimensions(inputs.shape[1]*3, 3)

    # Train the network
    network.train(filtered_inputs, filtered_outputs)

    # Save the network
    network.save('network.npy')
    network.save_as_csv('network.csv')

    print("network saved")
