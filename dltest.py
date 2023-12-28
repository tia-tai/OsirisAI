import numpy as np
import matplotlib.pyplot as plt


class NeuralNetwork:
    def __init__(self, learning_rate):
        self.weight = np.array([np.random.randn(), np.random.randn()])
        self.bias = np.random.randn()
        self.rate = learning_rate

    # Turns an int input into an output between 0 and 1
    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def _sigmoid_deriv(self, x):
        return self._sigmoid(x) * (1 - self._sigmoid(x))

    def gen_prediction(self, input):
        dot = np.dot(input, self.weight) + self.bias
        return self._sigmoid(dot)

    def _compute_gradients(self, input, target):
        dot = np.dot(input, self.weight) + self.bias
        prediction = self._sigmoid(dot)

        derror_dprediction = 2 * (prediction - target)
        dprediction_layer1 = self._sigmoid_deriv(dot)
        dbias_layer1 = 1
        dweight_layer1 = (0 * self.weight) + (1 * input)

        derror_dbias = derror_dprediction * dprediction_layer1 * dbias_layer1
        derror_dweight = derror_dprediction * dprediction_layer1 * dweight_layer1

        return derror_dbias, derror_dweight

    def _update_parameters(self, derror_dbias, derror_dweight):
        self.bias = self.bias - (derror_dbias * self.rate)
        self.weight = self.weight - (derror_dweight * self.rate)

    def train(self, inputs, targets, iterations):
        errors = []
        for x in range(iterations):
            # Randomly picks a data points
            data_index = np.random.randint(len(inputs))

            input = inputs[data_index]
            target = targets[data_index]

            # Computer gradients and update weights
            derror_dbias, derror_dweight = self._compute_gradients(input, target)

            self._update_parameters(derror_dbias, derror_dweight)

            # Collect the errors for all 100th iteration
            if x % 100 == 0:
                cumulative_error = 0

                for y in range(len(inputs)):
                    data_point = inputs[y]
                    target = targets[y]

                    prediction = self.gen_prediction(data_point)
                    error = np.square(prediction - target)

                    cumulative_error = cumulative_error + error
                errors.append(cumulative_error)

        return errors


inputs = np.array(
    [[3, 1.5], [2, 1], [4, 1.5], [3, 4], [3.5, 0.5], [2, 0.5], [5.5, 1], [1, 1]]
)
targets = np.array([0, 1, 0, 1, 0, 1, 1, 0])

nerual_network = NeuralNetwork(0.1)

error = nerual_network.train(inputs, targets, 1000000)


plt.plot(error)
plt.xlabel("Iterations in Hundreds")
plt.ylabel("Error per 100 Iterations")
plt.savefig("cum.png")
