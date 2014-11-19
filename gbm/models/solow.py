import numpy as np

from gbm.models.core import Parameter, Line, GraphBasedModel

class Solow(GraphBasedModel):
    def __init__(self):
        super(Solow, self).__init__(name='Solow', xlabel='capital ($)',
                                    ylabel='$')
        self.add(Parameter('A', 2, min=0, max=1000,
                           desc='Productivity'))
        self.add(Parameter('alpha', 0.5, min=0, max=1,
                           desc='Diminishing returns'))
        self.add(Parameter('s', 0.25, min=0, max=1, desc='Savings rate'))
        self.add(Parameter('d', 0.05, min=0, max=1, desc='Depreciation'))
        self.add(Parameter('n', 0.05, min=0, max=1, desc='Labor-force growth'))
        self.add(Parameter('k_max', 100, min=0, max=1000,
                           desc='Maximum capital'))

    def generate_data(self, p):
        steps = 200
        k = np.linspace(0, p.k_max, steps)
        output = p.A * (k ** p.alpha)
        investment = p.s * output
        break_even = (p.d + p.n) * k

        results = [
            Line(k, output, color='green', label='output per worker'),
            Line(k, investment, color='red', label='investment per worker'),
            Line(k, break_even, color='blue', label='break-even investment'),
            ]
        return results


if __name__ == '__main__':
    m = Solow()
    m.run()
