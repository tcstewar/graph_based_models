import numpy as np

from gbm.models.core import Parameter, Line, GraphBasedModel

class Bifurcate(GraphBasedModel):
    def __init__(self):
        super(Bifurcate, self).__init__(name='Bifurcation',
                                    ylabel='equilibrium',
                                    xlabel='a')
        self.add(Parameter('la', 0.3, min=0, max=1,
                           desc='lambda'))
        self.add(Parameter('b', 0.22, min=0, max=1,
                           desc='b'))
        self.add(Parameter('mu', 3.0, min=0, max=10,
                           desc='mu'))

    def expected_price(self, p_e0, a, p):
        return (1-p.la)*p_e0 + p.la*a/p.b - p.la*np.arctan(p.mu*p_e0)/p.b

    def generate_data(self, p):
        steps = 100
        a = np.linspace(0, 1, steps)

        x0 = 0.01
        sampling_start_time = 1000

        result_a = []
        result_x = []

        x = np.zeros_like(a) + x0
        for t in xrange(sampling_start_time):
            x = self.expected_price(x, a, p)

        data = []
        for t in xrange(6):   # number of sample line to draw
            x = self.expected_price(x, a, p)
            data.append(x)

        # sort the data so we can turn each row into a line
        data = np.array(data)
        data.sort(axis=0)

        lines = []
        for i in range(len(data)):
            label = 'bifurcate' if i==0 else 'dummy_%d' % i   # dummy labels are not shown
            lines.append(Line(a, data[i], color='blue', label=label))

        return lines





        x1 = x
        x2 = self.expected_price(x1, a, p)

        x_top = np.where(x1 > x2, x1, x2)
        x_bottom = np.where(x1 < x2, x1, x2)

        line1 = Line(a, x_top, color='blue', label='bifurcation (top)')
        line2 = Line(a, x_bottom, color='blue', label='bifurcation (bottom)')

        return [line1, line2]


if __name__ == '__main__':
    m = Bifurcate()
    r = m.run()
    m.plot_pylab(r)
