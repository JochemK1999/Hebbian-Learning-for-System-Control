import numpy as np

class HebbianNetwork():
    def __init__(self, numInputs=None, numOutputs=None, weights_file=None):
        if weights_file is not None:
            self.weights = np.load(weights_file)
        elif numInputs is not None and numOutputs is not None:
            self.weights = np.zeros((numInputs, numOutputs))
        else:
            raise ValueError("Either provide 'weights_file' or both 'numInputs' and 'numOutputs'.")

    @classmethod
    def from_file(cls, weights_file):
        return cls(weights_file=weights_file)

    @classmethod
    def from_dimensions(cls, numInputs, numOutputs):
        return cls(numInputs=numInputs, numOutputs=numOutputs)
    
    def train(self, inputs, labels, learning_rate=0.1, epochs=1):
        transformed_inputs = np.array([self.input_to_network(input) for input in  inputs])
        transformed_outputs = np.array([self.output_to_network(label) for label in labels])

        for _ in range(epochs):
            for index in range(len(inputs)):
                #Basic learning rule
                #self.weights += learning_rate * np.outer(transformed_inputs[i], transformed_outputs[i])
                for i in range(len(transformed_inputs[index])):
                    for j in range(len(transformed_outputs[index])):
                        self.weights[i][j] += learning_rate * transformed_outputs[index][j] * (transformed_inputs[index][i] - transformed_outputs[index][j] *self.weights[i][j])


        print(self.weights)
    
    def input_to_network(self, input):
        network_input = np.full(input.shape[0]*3, 0)
    
        for inputIndex, value in enumerate(input):
            if value == 1:
                network_input[inputIndex] = 1
            elif value == 2:
                network_input[inputIndex+input.shape[0]] = 1
            elif value == 3:
                network_input[inputIndex+2*input.shape[0]] = 1

        #print(network_input)

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
        print(self.weights.shape)
        output = np.dot(transformed_input, self.weights)

        return self.network_to_output(output)