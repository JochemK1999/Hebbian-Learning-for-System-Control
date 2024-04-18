import numpy as np
import math

class HebbianNetwork():
    def __init__(self, numInputs=None, numOutputs=None, weights_file=None):
        if weights_file is not None:
            self.weights = np.load(weights_file)
        elif numInputs is not None and numOutputs is not None:
            self.weights = np.zeros((self.get_input_nodes_count(numInputs), numOutputs))
        else:
            raise ValueError("Either provide 'weights_file' or both 'numInputs' and 'numOutputs'.")

    @classmethod
    def from_file(cls, weights_file):
        return cls(weights_file=weights_file)

    @classmethod
    def from_dimensions(cls, numInputs, numOutputs):
        return cls(numInputs=numInputs, numOutputs=numOutputs)

    def get_input_nodes_count(self, numInputs):
        return numInputs + math.comb(numInputs, 2)
    
    def train(self, inputs, labels, learning_rate=0.1, epochs=1, store_between_epochs=False):
        transformed_inputs = np.array([self.input_to_network(input) for input in  inputs])
        transformed_outputs = np.array([self.output_to_network(label) for label in labels])

        print("start training")

        for epoch in range(epochs):
            positive_update_sum = 0
            negative_update_sum = 0

            temp_weights = []
            for index in range(len(inputs)):
                #Basic learning rule
                #self.weights += learning_rate * np.outer(transformed_inputs[i], transformed_outputs[i])
                for i in range(len(transformed_inputs[index])):
                    for j in range(len(transformed_outputs[index])):
                        update = learning_rate * transformed_outputs[index][j] * (transformed_inputs[index][i] - transformed_outputs[index][j]*self.weights[i][j])
                        self.weights[i][j] += update
                        if update > 0:
                            positive_update_sum += update
                        else:
                            negative_update_sum += update
                        
                        if (i==23 and j==3 and transformed_outputs[index][j] == 1):
                            #print(f"input: {transformed_inputs[index][i]}, update weight: {update}, new weight: {self.weights[i][j]}")
                            temp_weights.append(self.weights[i][j])

                if (index%100==0):
                    print(index)

            print(positive_update_sum, negative_update_sum)
            self.save(f"network_lr_{learning_rate}_ep_{epoch+1}.npy")
            np.savetxt(f"WeightOverTime_ep_{epoch+1}.csv", temp_weights, delimiter=",")
    
    def input_to_network(self, input):
        network_input = np.full(self.get_input_nodes_count(input.shape[0]*3), 0)
    
        for inputIndex, value in enumerate(input):
            if value == 1:
                network_input[inputIndex] = 1
            elif value == 2:
                network_input[inputIndex+input.shape[0]] = 1
            elif value == 3:
                network_input[inputIndex+2*input.shape[0]] = 1

        index = 0
        for i in range(input.shape[0]*3):
            for j in range(i+1, input.shape[0]*3):
                network_input[input.shape[0]*3 + index] = network_input[i]*network_input[j]
                index += 1

        return network_input

    def output_to_network(self, output):
        network_output = np.zeros(4)
        
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
    
    def predict(self, input):
        transformed_input = self.input_to_network(np.array(input))
        output = np.dot(transformed_input, self.weights)
        print(output)
        return self.network_to_output(output)

if __name__ == "__main__":
    network = HebbianNetwork.from_file('network_lr_0.001_ep_2.npy')
    
    input = np.array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0])

    network_input = network.input_to_network(input)

    detector_names = []
    for i in range(3):
        for j in range(input.shape[0]):
            detector_names.append(f"d{j+1}_{i+1}")

    for i in range(input.shape[0]*3):
        for j in range(i+1, input.shape[0]*3):
            detector_names.append(detector_names[i] + "*" + detector_names[j])

    important_weights = []
    for index, (node, name) in enumerate(zip(network_input, detector_names)):
        if node != 0:
            important_weights.append([name] + list(network.weights[index]))
    
    for i in important_weights:
        print(i)
