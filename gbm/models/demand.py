import numpy as np

from gbm.models.core import Parameter, Line, GraphBasedModel

class DemandCurve(GraphBasedModel):
    def __init__(self):
        super(DemandCurve, self).__init__(name='Demand Curve',
                                    xlabel='price ($)',
                                    ylabel='amount produced')
        self.add(Parameter('p_max', 50, min=0, max=100,
                           desc='Maximum Price'))
        self.add(Parameter('q_max', 50, min=0, max=100,
                           desc='Maximum Quantity'))
        self.add(Parameter('quantity', 20, min=0, max=100,
                           desc='Actual Quantity'))

    def generate_data(self, p):
        steps = 200
        pp = np.linspace(0, p.p_max, steps)
        slope = - p.q_max / p.p_max
        demand = slope * pp + p.q_max

        price = (p.quantity - p.q_max ) / slope

        results = [
            Line(demand, pp, color='green', label='demand'),
            Line([0, p.quantity], [price, price], color='blue', label='price'),
            Line([p.quantity, p.quantity], [0, price], color='red', label='quantity'),
            ]

        return results


if __name__ == '__main__':
    m = DemandCurve()
    r = m.run()
    m.plot_pylab(r)
