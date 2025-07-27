from bottle import Bottle, HTTPResponse, default_app, post, request, run, route, template, debug, static_file, \
    BaseTemplate
from html import escape
from urllib.parse import urlencode, urlparse, parse_qs, parse_qsl
from config import *

import os
import sys
import shutil
from shutil import copy

import utils

dirname = os.path.dirname(os.path.abspath(__file__))

# add version and start timestamp to footer
BaseTemplate.defaults['FOOTER_INFO'] = utils.add_time_and_version()

x = list(vars(parmz).keys())

for f in [v for v in list(vars(parmz).keys()) if not v.startswith('__')]:
    BaseTemplate.defaults[f] = getattr(parmz, f)


@route(r'/static/<filename:re:.*\.(ico|jpg|png|gif|svg)>')
def send_ico(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join('static', 'asset', 'images'))


@route(r'/static/<filename:re:.*\.css(.map)?>')
def send_css(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join('static', 'asset', 'css'))


@route(r'/static/<filename:re:.*\.js(.map)?>')
def send_js(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join('static', 'asset', 'js'))


@route(r'/webfonts/<filename:re:.*\.(woff2?|ttf|svg)>')
def send_font(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join('static', 'asset', 'webfonts'))


@route('/' + parmz.IMAGE_DIRECTORY + '/<filename:re:.*>')
def send_image(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join(parmz.IMAGE_DIRECTORY))


@route('/')
def index(data=None):
    if data is None:
        data = {'home': 'here'}
    parameters = request.forms
    if parameters == {}:
        parameters = {'terms': [('*', '*')],
                      'controls': {},
                      'result_fields': [p[1] for p in FIELD_DEFINITIONS['LIST']],
                      'facet_fields': [p[1] for p in FIELD_DEFINITIONS['FACETS']]
                      }
    data['selected_field'] = ''
    data['query_string'] = ''
    data['results'] = utils.query(parameters)
    data['terms'] = []
    controls = parameters['controls']
    data['content'] = data['results']['results']
    return utils.check_template('index', data, controls, request.forms)


@route('/about')
def about():
    data = {'about': 'here'}
    return index(data)


@route('/facet/')
@route('/search/', method=['GET', 'POST'])
def facet():
    terms = []
    r = request
    query = parse_qsl(request.query_string)
    control_names = 'display page per_page view'.split(' ')
    controls = {}

    if request.POST != {}:
        parsed_url = urlparse(request.POST['query_string'])
        query = parse_qs(parsed_url.path)
        for q in query:
            query[q] = query[q][0]
        terms.append((request.POST['search_field'], request.POST['search_value']))
    for f in query:
        if f[0] in control_names:
            try:
                controls[f[0]] = int(f[1])
            except:
                controls[f[0]] = f[1]
        else:
            terms.append(f)

    # assign defaults if necessary
    if not 'page' in controls: controls['page'] = 1
    if not 'per_page' in controls: controls['per_page'] = 80
    if not 'view' in controls: controls['view'] = 'LIST'  # Default to 'LIST' if not set
    current_view = controls['view']

    parameters = {'result_fields': [p[1] for p in FIELD_DEFINITIONS[current_view]],
                  'facet_fields': [p[1] for p in parmz.FACETS],
                  'terms': terms,
                  'controls': controls
                  }
    data = {}
    data['results'] = utils.query(parameters)
    data['selected_field'] = ''
    data['result_fields'] = FIELD_DEFINITIONS[current_view]
    data['terms'] = terms
    data['controls'] = controls
    data['query_string'] = urlencode(terms) + '&' + urlencode(controls)
    data['base_string'] = urlencode(terms)
    data['image_field'] = parmz.IMAGE_FIELD
    # data['query_string'] = '?' + '&'.join([urlencode(terms), urlencode(controls)])
    data['content'] = data['results']['results']
    return utils.check_template('index', data, controls, request)


@route('/single/<term:re:.*>')
def single(term):
    term = [('KEY_s', term.replace('_', ' '))]
    controls = {}

    parameters = {'result_fields': [p[1] for p in FIELD_DEFINITIONS['FULL']],
                  'facet_fields': [p[1] for p in parmz.FACETS],
                  'terms': term,
                  'controls': controls
                  }
    data = {}
    data['results'] = utils.query(parameters)
    data['selected_field'] = ''
    data['result_fields'] = FIELD_DEFINITIONS['FULL']
    data['terms'] = term
    data['controls'] = controls
    data['query_string'] = urlencode(term | controls)
    data['base_string'] = urlencode(term)
    data['image_field'] = parmz.IMAGE_FIELD
    data['single'] = data['results']['results'][0]
    return utils.check_template('index', data, controls, request)


@route('/remove/<term:re:.*>')
def remove(term):
    r = request
    query = dict(request.query.decode())
    return index(data)
    # return utils.check_template('index', data, request.forms)


def download(full_path, filename):
    content = utils.all_file_content(full_path)
    response = HTTPResponse()
    response.body = content
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response


# run(server='gunicorn', port=parmz.PORT)
if __name__ == '__main__':
    run(host='0.0.0.0', port=parmz.PORT)
