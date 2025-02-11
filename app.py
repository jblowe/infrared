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
BaseTemplate.defaults['footer_info'] = utils.add_time_and_version()

x = list(vars(parmz).keys())

for f in [v for v in list(vars(parmz).keys()) if not v.startswith('__')]:
    BaseTemplate.defaults[f] = getattr(parmz, f)


@route('/static/<filename:re:.*\.(ico|jpg|png|gif)>')
def send_ico(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join('static', 'asset', 'images'))


@route('/static/<filename:re:.*\.css(.map)?>')
def send_css(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join('static', 'asset', 'css'))


@route('/static/<filename:re:.*\.js(.map)?>')
def send_js(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join('static', 'asset', 'js'))


@route('/webfonts/<filename:re:.*\.(woff2?|ttf|svg)>')
def send_font(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join('static', 'asset', 'webfonts'))


@route('/')
def index(data=None):
    if data is None:
        data = {'home': 'here'}
    parameters = request.forms
    if parameters == {}:
        parameters = {'terms': {'*': '*'},
                      'result_fields': [p[1] for p in FIELD_DEFINITIONS['LIST']],
                      'facet_fields': [p[1] for p in FIELD_DEFINITIONS['FACETS']]
                      }
    data['selected_field'] = ''
    data['query_string'] = 'facet/?'
    data['results'] = utils.query(parameters)
    del parameters['terms']['*']
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
    parameters = {
        'result_fields': [p[1] for p in parmz.LIST],
        'facet_fields': [p[1] for p in parmz.FACETS]
    }
    control_names = 'display start_page per_page'.split(' ')
    to_remove = set()
    controls = {}
    for f in query:
        if f in control_names:
            controls[c] = query[f]
        elif f == 'remove':
            to_remove.add(query[f])
        else:
            terms[f] = query[f]
    for s in to_remove:
        del terms[s]
    parameters['terms'] = terms
    data = {}
    data['selected_field'] = ''
    data['query_string'] = '?' + urlencode(terms) + '&' + urlencode(controls)
    data['results'] = utils.query(parameters)
    data['content'] = data['results']['results']
    return utils.check_template('index', data, request.forms)


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
run()
