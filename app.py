from bottle import Bottle, HTTPResponse, default_app, post, request, run, route, template, debug, static_file, \
    BaseTemplate
from html import escape
from urllib.parse import urlencode
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


@route(r'/static/<filename:re:.*\.(ico|jpg|png|gif)>')
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


@route('/images/<filename:re:.*>')
def send_image(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join('images'))


@route('/')
def index(data=None):
    if data is None:
        data = {'home': 'here'}
    parameters = request.forms
    if parameters == {}:
        parameters = {'terms': {'*': '*'},
                      'controls': {},
                      'result_fields': [p[1] for p in FIELD_DEFINITIONS['LIST']],
                      'facet_fields': [p[1] for p in FIELD_DEFINITIONS['FACETS']]
                      }
    data['selected_field'] = ''
    data['query_string'] = ''
    data['results'] = utils.query(parameters)
    data['terms'] = parameters['terms']
    del data['terms']['*']
    data['controls'] = parameters['controls']
    data['content'] = data['results']['results']
    return utils.check_template('index', data, request.forms)


@route('/about')
def about():
    data = {'about': 'here'}
    return index(data)


@route('/facet/')
@route('/search/')
def facet():
    terms = {}
    r = request
    query = dict(request.query.decode())
    control_names = 'display start_page per_page view'.split(' ')
    controls = {}

    base_query = dict(request.query)
    current_view = query.get('view', 'FULL').upper()  # Default to 'FULL' if not set
    query['view'] = current_view
    base_query.pop('view', None)

    if 'search' in query:
        terms[query['search_field']] = query['search_value']
        del query['search']
        del query['search_field']
        del query['search_value']
    for f in query:
        if f in control_names:
            controls[f] = query[f]
        else:
            terms[f] = query[f]

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
    x = terms | controls
    data['query_string'] = urlencode(terms | controls)
    data['base_string'] = urlencode(base_query)
    data['image_field'] = parmz.IMAGE_FIELD
    # data['query_string'] = '?' + '&'.join([urlencode(terms), urlencode(controls)])
    data['content'] = data['results']['results']
    return utils.check_template('index', data, request)


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


# application = default_app()
run(host='0.0.0.0', port=parmz.PORT)
