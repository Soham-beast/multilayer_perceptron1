import numpy as np


class Affine:
    def __init__(self, input_size, output_size, lr_rate):
        self.x = None
        self.w = np.random.randn(input_size, output_size) / np.sqrt(input_size)
        rng = np.random.default_rng()
        self.b = np.zeros(output_size)
        self.lr_rate = lr_rate

    def forward(self, x):
        self.x = x
        return np.dot(x, self.w) + self.b

    def backward(self, dx):
        dw = np.dot(self.x.T, dx)
        db = np.sum(dx, axis=0)
        self.w = self.w - np.dot(self.lr_rate, dw)
        self.b = self.b - np.dot(self.lr_rate, db)
        res = np.dot(dx, self.w.T)
        return res


class Sigmoid:
    def __init__(self):
        self.out = None

    def forward(self, x):
        self.out = 1 / (1 + np.exp(-x))
        return self.out

    def backward(self, dx):
        res = dx * (1 - self.out) * self.out
        return res


class Softmax:
    def __init__(self, input_size, output_size):
        self.x = None
        self.dx = np.zeros((input_size, output_size))

    def forward(self, x):
        exp_sum = np.sum(np.exp(x), axis=1)
        for i in range(x.shape[0]):
            x[i, :] = np.exp(x[i, :]) / exp_sum[i]

        self.x = x
        return x

    def backward(self, label):
        for i in range(self.x.shape[0]):
            if label[i] == 1:
                self.dx[i] = np.array([self.x[i, 0]-1, self.x[i, 1]-0])
            else:
                self.dx[i] = np.array([self.x[i, 0]-0, self.x[i, 1]-1])

        return self.dx


class BinaryCrossEntropy:
    def forward(self, x, label):
        loss_sum = 0
        for i in range(x.shape[0]):
            prob = x[i, :][0]
            loss_sum += label[i] * np.log(prob) + (1 - label[i]) * np.log(1 - prob)

        return (-1) * loss_sum / x.shape[0]
