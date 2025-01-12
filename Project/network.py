# Python libraries used
import random
import math

# Fitness funtion
from fitness import RankChromosomes

# Class for each layer
class Layer:
    def __init__(self, inputs_count, outputs_count):
        # Number of outputs
        self.outputs = [0.0 for _ in range(outputs_count)]

        # Matrix for each neuron's weights
        self.weights = [[random.random() * 2 - 1 for _i in range(inputs_count)] for _o in range(outputs_count)]

    # Output calculation
    def feed_forward(self, inputs):
        for output_index, output in enumerate(self.outputs):
            sum = 0
            for weight_index, input in enumerate(inputs):
                sum += self.weights[output_index][weight_index] * input

            # Limits values between 0 and 1
            self.outputs[output_index] = math.tanh(sum) # activation function similer to sigmoid

# Neural network
class Network:
    def __init__(self, dimensions):
        self.reached_goal = False

        # Dimensions is # of neurons per layer(len() is # of layers + 1)
        self.dimensions = dimensions

        # Layer calculation
        self.layers = []

        for i in range(len(dimensions) - 1):
            self.layers.append(Layer(dimensions[i], dimensions[i + 1]))

    # Output calculation
    def feed_forward(self, inputs):
        # HUD stuff
        self.inputs = [i for i in inputs]

        # loops through each layer
        for layer in self.layers:
            # Finds outputs of each layer
            layer.feed_forward(inputs)
            inputs = [i for i in layer.outputs]
        
        # Returns output of last layer
        return self.layers[-1].outputs
    
    # Ranks chromosomes
    def serialize(self):
        chromosomes = []

        for layer in self.layers:
            for outputs in layer.weights:
                for weight in outputs:
                    chromosomes.append(weight)
        
        # Returns the ranked chromosomes
        return RankChromosomes(self.highest_checkpoint, chromosomes)
    
    # Updates chromosomes
    def deserialize(self, chromosome):
        layer_index = 0
        output_index = 0
        input_index = 0
        for gene in chromosome:
            self.layers[layer_index].weights[output_index][input_index] = gene

            input_index += 1

            if input_index > len(self.layers[layer_index].weights[output_index]) - 1:
                output_index += 1
                input_index = 0

                if  output_index > len(self.layers[layer_index].weights) - 1:
                    layer_index += 1
                    output_index = 0