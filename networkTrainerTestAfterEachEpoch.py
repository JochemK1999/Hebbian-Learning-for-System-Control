import numpy as np
import pandas as pd

from HebbianNetwork import HebbianNetwork

df2 = pd.read_csv('1-2InputJumpDuckOutputTest.csv')
#df2 = pd.read_csv('LowObject6DetectorsLJTest.csv')

# Extract inputs (first 10 columns) and outputs (last column) as NumPy arrays
test_inputs = df2.iloc[:, :-1].values  # Extract all rows and all but the last column
test_outputs = df2.iloc[:, -1].values  # Extract all rows and the last column

counter = 0

def test_network():
    global counter
    faults = []
    for input, output in zip(test_inputs, test_outputs):
        network_output = network.predict(input)
        if network_output != output:
            faults.append(f"{input}, {network_output}, {output}")
    
    print(f"epoch: {counter}, inputs: {len(test_inputs)}, faults: {len(faults)}, ratio: {(len(test_inputs)-len(faults))/len(test_inputs)}")
    # print(faults)
    counter += 1


if __name__ == "__main__":
    df = pd.read_csv('random_rows.csv')
    #df = pd.read_csv('1-2InputJumpDuckOutput.csv')
    #df = pd.read_csv('LowObject6DetectorsLJTraining.csv')

    # Extract inputs (first 10 columns) and outputs (last column) as NumPy arrays
    inputs = df.iloc[:, :-1].values  # Extract all rows and all but the last column
    outputs = df.iloc[:, -1].values  # Extract all rows and the last column

    # Create a network with 30 inputs and 3 outputs
    print(inputs.shape[1]*3)

    network = HebbianNetwork.from_dimensions(inputs.shape[1]*3, 4, combinations=False, batch_training = False)

    test_network()
    
    for i in range(40):
        # Train the network"
        network.train(inputs, outputs, learning_rate=0.001, epochs=1, resample=False)

        test_network()

    network.save("network.npy")