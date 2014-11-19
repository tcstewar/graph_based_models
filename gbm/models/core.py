import collections

class Parameter(object):
    def __init__(self, name, default, min, max, desc, decimals=2):
        self.name = name
        self.default = default
        self.min = min
        self.max = max
        self.desc = desc
        self.decimals = decimals

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
    def __init__(self, name, xlabel, ylabel):
        self.params = collections.OrderedDict()
        self.name = name
        self.xlabel = xlabel
        self.ylabel = ylabel

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

    def html_sliders(self):
        sliders = []
        for k, p in self.params.items():
            html = '''<div class="slider_label">%(desc)s:
                           <span id="s_val_%(k)s" class="s_value">
                           %(default)g</span>
                      </div>
                      <div id="s_%(k)s" class="slider"></div>
                      <script>d3.select("#s_%(k)s").call(d3.slider()
                          .axis(true).value(%(default)g)
                          .on("slide", function(evt,value) {
                              update_slide('%(k)s', value, %(decimals)d);})
                          .min(%(min)g)
                          .max(%(max)g));
                      </script>
                      ''' % dict(desc=p.desc, k=k, default=p.default,
                                 min=p.min, max=p.max, decimals=p.decimals)
            sliders.append(html)

        return ''.join(sliders)

