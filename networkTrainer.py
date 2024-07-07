import numpy as np
import pandas as pd

from HebbianNetwork import HebbianNetwork

if __name__ == "__main__":
    #Set the dataset to be used
    #dataset = pd.read_csv('LowObstacleGame_SJ_Data.csv')
    dataset = pd.read_csv('LowObstacleGame_SJ+LJ_Data.csv')
    #dataset = pd.read_csv('AllObstacleGame_Data.csv')
    #dataset = pd.read_csv('AllObstacleGame_Resampled_Data.csv')

    #Set the validation set to be used
    #validationSet = pd.read_csv('LowObstacleGame_SJ_Validation.csv')
    validationSet = pd.read_csv('LowObstacleGame_SJ+LJ_Validation.csv')
    #validationSet = pd.read_csv('AllObstacleGame_Validation.csv')

    # Extract inputs (first 10 columns) and outputs (last column) as NumPy arrays
    inputs = dataset.iloc[:, :-1].values  # Extract all rows and all but the last column
    outputs = dataset.iloc[:, -1].values  # Extract all rows and the last column

    # Create a network with 30 inputs and 3 outputs
    print(inputs.shape[1]*3)

    network = HebbianNetwork.from_dimensions(inputs.shape[1]*3, 4, combinations=False, batch_training = False)

    # Train the network"
    network.train(inputs, outputs, learning_rate=0.01, epochs=30, resample=False)

    # Save the network
    network.save('network.npy')
    network.save_as_csv('network.csv')

    # Extract inputs (first 10 columns) and outputs (last column) as NumPy arrays
    test_inputs = validationSet.iloc[:, :-1].values  # Extract all rows and all but the last column
    test_outputs = validationSet.iloc[:, -1].values  # Extract all rows and the last column

    faults = []

    for input, output in zip(test_inputs, test_outputs):
        network_output = network.predict(input)
        if network_output != output:
            wrong_dataset = f"{input}, {network_output}, {output}"
            if wrong_dataset not in faults:
                faults.append(wrong_dataset)
    
    for i in faults:
        print(i)

    print("network saved")
