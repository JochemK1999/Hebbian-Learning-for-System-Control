import numpy as np
import pandas as pd

from HebbianNetwork import HebbianNetwork

if __name__ == "__main__":
    df = pd.read_csv('filtered_data.csv')

    print(df.shape)

    # Extract inputs (first 10 columns) and outputs (last column) as NumPy arrays
    inputs = df.iloc[:, :-1].values  # Extract all rows and all but the last column
    outputs = df.iloc[:, -1].values  # Extract all rows and the last column

    print(inputs.shape)

    # Create a network with 30 inputs and 3 outputs
    network = HebbianNetwork.from_dimensions(inputs.shape[1]*3, 4)

    # Train the network
    network.train(inputs, outputs)

    # Save the network
    network.save('network.npy')
    network.save_as_csv('network.csv')

    print("network saved")
