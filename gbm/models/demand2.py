import numpy as np

from gbm.models.core import Parameter, Line, GraphBasedModel

class DemandTwoSuppliers(GraphBasedModel):
    def __init__(self):
        super(DemandTwoSuppliers, self).__init__(name='Demand Curve',
                                    ylabel='Price ($)',
                                    xlabel='Quantity (MM 18lb units)')
        self.add(Parameter('a', 30, min=0.01, max=50,
                           desc='Choke price, $/18lb unit (a)'))
        self.add(Parameter('b', 8, min=0.01, max=1000,
                           desc='Slope of demand curve (b)'))
        self.add(Parameter('d', 0.33, min=0.01, max=1.5,
                           desc='Market power of local (d)'))
        self.add(Parameter('ga', 1, min=0.01, max=5,
                           desc='Competition (gamma)'))
        self.add(Parameter('pe', 16, min=0.01, max=30,
                           desc='Mean expected import price, $/18lb unit (pe)'))
        self.add(Parameter('plocal', 17, min=0.01, max=30,
                           desc='Price chosen by the marketing board, $/18lb unit (pe)'))


    def generate_data(self, p):
        steps = 200
        qq = np.linspace(0, 2.0, steps)

        pe_line = [p.pe for i in range(0,steps)]


        pe_plt = p.pe*np.ones(steps)

        demand_basic = p.a - p.b * qq
        
        demand_local = p.pe + p.d * (p.a-p.pe)*qq

        d_intercept = p.pe + p.d*(p.a - p.pe)

        results = [
            Line([0, p.a/p.b], [p.a,0], color='gray', label='Demand'),
            Line([0,(p.a - p.pe)/p.b], [p.pe, p.pe], color='blue', label='Expected California Price'),
            Line([(p.a - p.pe)/p.b,(p.a - p.pe)/p.b], [0, p.pe], color='blue',label='Q Just California'),
            Line([0,(p.a - p.pe)/p.b], [d_intercept, p.pe], color='red', label='Local Demand'),
            Line([0,(p.a - p.plocal)/p.b], [p.plocal, p.plocal], color='gray', label='Marketing Board Chooses'),
            Line([(p.a - p.plocal)/p.b,(p.a - p.plocal)/p.b], [0, p.plocal], color='gray', label='Q Local'),
            ]

        return results


if __name__ == '__main__':
    m = DemandTwoSuppliers()
    r = m.run()
    m.plot_pylab(r)