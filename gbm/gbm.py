import numpy as np

class Parameter(object):
    def __init__(self, name, default, min, max, desc):
        self.name = name
        self.default = default
        self.min = min
        self.max = max

class ParamSet(object):
    def __init__(self, params, overrides):
        for k, v in params.items():
            value = overrides.get(k, v.default)
            setattr(self, k, value)

class Line(object):
    def __init__(self, x, y, color, label):
        self.x = x
        self.y = y
        self.color = color
        self.label = label

class GraphBasedModel(object):
    def __init__(self):
        self.params = {}
    def add(self, obj):
        if isinstance(obj, Parameter):
            self.params[obj.name] = obj

    def run(self, **params):
        p = ParamSet(self.params, params)
        r = self.generate_data(p)

        import pylab
        for line in r:
            pylab.plot(line.x, line.y, color=line.color, label=line.label)
        pylab.show()



class SolowModel(GraphBasedModel):
    def __init__(self):
        super(SolowModel, self).__init__()
        self.add(Parameter('A', 2, min=0, max=1000, desc='Productivity'))
        self.add(Parameter('alpha', 0.5, min=0, max=1, desc='Diminishing returns'))
        self.add(Parameter('s', 0.25, min=0, max=1, desc='Savings rate'))
        self.add(Parameter('d', 0.05, min=0, max=1, desc='Depreciation'))
        self.add(Parameter('n', 0.05, min=0, max=1, desc='Labor-force growth'))
        self.add(Parameter('k_max', 100, min=0, max=1000, desc='Maximum capital'))

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
    m = SolowModel()
    m.run()





