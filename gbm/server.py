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

        return html % dict(sliders=sliders, model_name=model.name,
                           xlabel=model.xlabel, ylabel=model.ylabel)



