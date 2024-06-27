import numpy as np
import math
from collections import Counter
from random import choices
import random

class HebbianNetwork():
    def __init__(self, numInputs=None, numOutputs=None, combinations=False, weights_file=None, batch_training=False):
        self.combinations = combinations
        self.batch_training = batch_training
        if weights_file is not None:
            self.weights = np.load(weights_file)
            if self.weights.shape[0] > 100:
                combinations = True
        elif numInputs is not None and numOutputs is not None:
            if (combinations):
                self.weights = np.zeros((self.get_input_nodes_count(numInputs), numOutputs))
            else:
                self.weights = np.zeros((numInputs, numOutputs))
        else:
            raise ValueError("Either provide 'weights_file' or both 'numInputs' and 'numOutputs'.")

    @classmethod
    def from_file(cls, weights_file):
        return cls(weights_file=weights_file)

    @classmethod
    def from_dimensions(cls, numInputs, numOutputs, combinations=False, batch_training=False):
        return cls(numInputs=numInputs, numOutputs=numOutputs, combinations=combinations, batch_training=batch_training)

    def get_input_nodes_count(self, numInputs):
        return numInputs + math.comb(numInputs, 2)
    
    def resample(self, inputs, outputs):
        # Count the number of occurrences of each class
        counter = Counter(outputs)

        print(counter)

        # Find the maximum count
        max_count = max(counter.values())

        # Resample each class to have the same number of samples as the maximum count
        resampledInputs = []
        resampledOutputs = []
        
        for class_value, count in counter.items():
            # Find the indices of samples of this class
            indices = [i for i, x in enumerate(outputs) if x == class_value]

            if count < max_count:
                # Resample the indices
                resampledIndices = choices(indices, k=max_count)
            else:
                # If this is the majority class, just use the original indices
                resampledIndices = indices

            # Add the resampled inputs and outputs to the resampled lists
            resampledInputs.extend([inputs[i] for i in resampledIndices])
            resampledOutputs.extend([outputs[i] for i in resampledIndices])

        # Combine the resampled inputs and outputs into pairs
        combined = list(zip(resampledInputs, resampledOutputs))

        # Shuffle the combined list
        random.shuffle(combined)

        # Separate the shuffled inputs and outputs
        shuffledInputs, shuffledOutputs = zip(*combined)

        #print("waaaaaaaaa: ", len(outputs), len(shuffledOutputs))

        return list(shuffledInputs), list(shuffledOutputs)

    def train(self, inputs, labels, learning_rate=0.1, epochs=1, store_between_epochs=False, resample=False):
        if resample:
            inputs, labels = self.resample(inputs, labels)

        transformed_inputs = np.array([self.input_to_network(input) for input in  inputs])
        transformed_outputs = np.array([self.output_to_network(label) for label in labels])

        #print("start training")

        temp_weights = []
        for epoch in range(epochs):
            update_matrix = np.zeros(self.weights.shape)

            for index in range(len(inputs)):
                #Basic learning rule
                #self.weights += learning_rate * np.outer(transformed_inputs[i], transformed_outputs[i])
                for i in range(len(transformed_inputs[index])):
                    for j in range(len(transformed_outputs[index])):
                        # Normal rule 
                        update = learning_rate * transformed_outputs[index][j] * (transformed_inputs[index][i] - transformed_outputs[index][j]*self.weights[i][j])
                        
                        # Power rule
                        #update = learning_rate * transformed_outputs[index][j] * ((transformed_inputs[index][i] - transformed_outputs[index][j]*self.weights[i][j])**5)
                        
                        # Normal rule 
                        update = learning_rate * transformed_outputs[index][j] * (transformed_inputs[index][i] - transformed_outputs[index][j]*self.weights[i][j])
                        
                        if self.batch_training:
                            update_matrix[i][j] += update
                        else:
                            self.weights[i][j] += update

                if not self.batch_training:
                    temp_weights.append(self.weights.flatten())

                if (index%100==0):
                    pass
                    #print(index)
            
            if self.batch_training:
                self.weights += update_matrix
                temp_weights.append(self.weights.flatten())

            #self.save(f"network_lr_{learning_rate}_ep_{epoch+1}.npy")
        np.savetxt(f"WeightOverTime.csv", temp_weights, delimiter=",")
    
    def input_to_network(self, input):
        if self.combinations:
            network_input = np.full(self.get_input_nodes_count(input.shape[0]*3), -1)
        else:
            network_input = np.full(input.shape[0]*3, -1)

        for inputIndex, value in enumerate(input):
            if value == 1:
                network_input[inputIndex] = 1
            elif value == 2:
                network_input[inputIndex+input.shape[0]] = 1
            elif value == 3:
                network_input[inputIndex+2*input.shape[0]] = 1

        if self.combinations:
            index = 0
            for i in range(input.shape[0]*3):
                for j in range(i+1, input.shape[0]*3):
                    network_input[input.shape[0]*3 + index] = network_input[i]*network_input[j]
                    index += 1

        return network_input

    def output_to_network(self, output):
        network_output = np.full(4, 0)
        
        if output == "nothing":
            network_output[0] = 1
        if output == "jump":
            network_output[1] = 1
        if output == "long_jump":
            network_output[2] = 1
        if output == "duck":
            network_output[3] = 1
        
        return network_output
    
    def network_to_output(self, output):
        if output[0] == max(output):
            return "nothing"
        if output[1] == max(output):
            return "jump"
        if output[2] == max(output):
            return "long_jump"
        if output[3] == max(output):
            return "duck"

    def save(self, filename):
        np.save(filename, self.weights)
    
    def save_as_csv(self, filename):
        np.savetxt(filename, self.weights, delimiter=",")
    
    def load(self, filename):
        self.weights = np.load(filename)
    
    def predict(self, input, verbose=False):
        transformed_input = self.input_to_network(np.array(input))
        network_output = np.dot(transformed_input, self.weights)
        
        output = self.network_to_output(network_output)
        return output

if __name__ == "__main__":
    network = HebbianNetwork.from_file('network.npy')
    
    input = np.array([2, -1, -1, -1, -1, -1])

    network_input = network.input_to_network(input)
    network_output = np.dot(network_input, network.weights)


    detector_names = []
    for i in range(3):
        for j in range(input.shape[0]):
            detector_names.append(f"d{j+1}_{i+1}")

    """
    for i in range(input.shape[0]*3):
        for j in range(i+1, input.shape[0]*3):
            detector_names.append(detector_names[i] + "*" + detector_names[j])
    """

    important_weights = []
    for index, (node, name) in enumerate(zip(network_input, detector_names)):
        if node != 0:
            important_weights.append([name] + list(network.weights[index]))
    
    for i in important_weights:
        print(i)

    print("----------------------------------------------")

    for name, output in zip(detector_names, network_output):
        print(name, output)
    
    
