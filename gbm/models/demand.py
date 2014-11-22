import numpy as np

from gbm.models.core import Parameter, Line, GraphBasedModel

class DemandCurve(GraphBasedModel):
    def __init__(self):
        super(DemandCurve, self).__init__(name='Demand Curve',
                                    ylabel='price ($)',
                                    xlabel='amount produced')
        self.add(Parameter('p_max', 50, min=0, max=100,
                           desc='Maximum Price'))
        self.add(Parameter('p_min', 10, min=0, max=100,
                           desc='Minimum Price'))
        self.add(Parameter('slope', 0.1, min=0, max=5,
                           desc='Price reduction'))
        self.add(Parameter('quantity', 200, min=0, max=700,
                           desc='Quantity'))

    def generate_data(self, p):
        steps = 200
        qq = np.linspace(0, 700, steps)

        price = -p.slope * qq + p.p_max
        price = np.maximum(price, p.p_min)

        target_price = -p.slope * p.quantity + p.p_max
        target_price = np.maximum(target_price, p.p_min)

        results = [
            Line(qq, price, color='green', label='demand'),
            Line([0, p.quantity], [target_price, target_price], color='blue', label='price'),
            Line([p.quantity, p.quantity], [0, target_price], color='red', label='quantity'),
            ]

        return results


if __name__ == '__main__':
    m = DemandCurve()
    r = m.run()
    m.plot_pylab(r)
