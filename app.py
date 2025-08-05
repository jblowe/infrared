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

for f in [v for v in list(vars(parmz).keys()) if not v.startswith('__')]:
    BaseTemplate.defaults[f] = getattr(parmz, f)


@route(r'/static/<filename:re:.*\.(ico|jpg|png|gif|svg)>')
def send_ico(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join('static', 'images'))


@route(r'/static/<filename:re:.*\.css(.map)?>')
def send_css(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join('static', 'css'))


@route(r'/static/<filename:re:.*\.js(.map)?>')
def send_js(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join('static', 'js'))


@route(r'/webfonts/<filename:re:.*\.(woff2?|ttf|svg)>')
def send_font(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join('static', 'webfonts'))


@route('/' + parmz.IMAGE_DIRECTORY + '/<filename:re:.*>')
def send_image(filename):
    return static_file(filename, root=dirname + os.sep + os.path.join(parmz.IMAGE_DIRECTORY))


@route('/')
def index(data=None):
    parameters = request.forms
    controls = utils.set_controls({})
    if parameters == {}:
        parameters = {'terms': [('*', '*')],
                      'controls': {},
                      'result_fields': [p[1] for p in FIELD_DEFINITIONS['LIST']],
                      'facet_fields': [p[1] for p in FIELD_DEFINITIONS['FACETS']]
                      }
    data = utils.set_parameters(parameters, FIELD_DEFINITIONS['FULL'], [], controls)
    data['home'] = 'here'
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
    query_dict = parse_qs(request.query_string)
    control_names = 'display page per_page view'.split(' ')
    controls = {}

    # handle injection of keyterm searches
    if 'search_field' in query_dict:
        parsed_url = urlparse(query_dict['query_string'][0])
        query = parse_qsl(parsed_url.path)
        try:
            terms.append((query_dict['search_field'][0], query_dict['search_value'][0]))
        except:
            terms.append((query_dict['search_field'][0], '*'))
    for f in query:
        if f[0] in control_names:
            try:
                controls[f[0]] = int(f[1])
            except:
                controls[f[0]] = f[1]
        else:
            terms.append(f)

    # assign defaults if necessary
    controls = utils.set_controls(controls)
    current_view = controls['view']

    parameters = {'result_fields': [p[1] for p in FIELD_DEFINITIONS[current_view]],
                  'facet_fields': [p[1] for p in parmz.FACETS],
                  'terms': terms,
                  'controls': controls
                  }

    data = utils.set_parameters(parameters, FIELD_DEFINITIONS[current_view], terms, controls)
    data['content'] = data['results']['results']
    return utils.check_template('index', data, controls, request)


@route('/single/<term:re:.*>')
def single(term):
    # nb: in this case, there is always only a single term: the key to the record
    term = [('id', term.replace('_', ' '))]
    controls = {}

    parameters = {'result_fields': [p[1] for p in FIELD_DEFINITIONS['FULL']],
                  'facet_fields': [p[1] for p in parmz.FACETS],
                  'terms': term,
                  'controls': controls
                  }

    data = utils.set_parameters(parameters, FIELD_DEFINITIONS['FULL'], term, controls)
    if data['results']['numfound'] == 0:
        data['errors'] = ['record not found, sorry!']
    else:
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

    import argparse

    parser = argparse.ArgumentParser(description="Run the Bottle app.")
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=3002)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    run(host=args.host, port=args.port, debug=args.debug)

