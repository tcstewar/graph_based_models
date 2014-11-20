import os.path
import json
import pkgutil

import gbm
import gbm.swi as swi

pkg = 'gbm'

class Server(swi.SimpleWebInterface):
    def swi_static(self, *path):
        if self.user is None: return
        fn = os.path.join('static', *path)
        if fn.endswith('.js'):
            mimetype = 'text/javascript'
        elif fn.endswith('.css'):
            mimetype = 'text/css'
        elif fn.endswith('.png'):
            mimetype = 'image/png'
        elif fn.endswith('.jpg'):
            mimetype = 'image/jpg'
        elif fn.endswith('.gif'):
            mimetype = 'image/gif'
        elif fn.endswith('.otf'):
            mimetype = 'font/font'
        else:
            raise Exception('unknown extenstion for %s' % fn)

        data = pkgutil.get_data(pkg, fn)
        return (mimetype, data)

    def swi(self):
        if self.user is None:
            return self.create_login_form()
        html = pkgutil.get_data(pkg, 'templates/index.html')

        models = []
        for k in dir(gbm.models):
            try:
                if issubclass(getattr(gbm.models, k),
                              gbm.models.core.GraphBasedModel):
                    models.append(k)
            except TypeError:
                pass

        links = ['<li><a href="run/%s">%s</a></li>' % (k, k) for k in models]
        model_list = ''.join(links)

        return html % dict(model_list=model_list)

    def swi_run(self, model):
        model = getattr(gbm.models, model)()

        html = pkgutil.get_data(pkg, 'templates/run.html')

        sliders = model.html_sliders()
        slider_keys = model.params.keys()

        return html % dict(sliders=sliders, model_name=model.name,
                           xlabel=model.xlabel, ylabel=model.ylabel,
                           slider_keys=slider_keys)

    def swi_run_json(self, model, **params):
        p = {}
        for k, v in params.items():
            if k.startswith('key_'):
                p[k[4:]] = float(v)

        model = getattr(gbm.models, model)()

        r = model.run(**p)
        data = model.plot_nvd3(r)

        return json.dumps(dict(main=data))


