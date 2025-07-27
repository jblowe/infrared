import os, time, sys, re
import lxml.etree as ET
from urllib.parse import urlencode

from bottle import template, redirect

from config import *
import solr_query
import subprocess

# nb: we are trying to get the directory above the directory this file is in
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_version():
    try:
        tag = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return tag
    except subprocess.CalledProcessError:
        return "no-tag"
    except FileNotFoundError:
        return "git-not-found"

def spaceless(rendered_html):
    return re.sub(r'>\s+<', '><', rendered_html.strip())


def add_time_and_version():
    return 'code and data version: %s, system last restarted: %s' % (
        get_version(), time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))


def check_template(tpl, data, controls, request):
    if 'back' not in data:
        data['back'] = '/'
    # redirect('/facet/' + data['query_string'])

    return template(spaceless(tpl), controls=controls, data=data)


def query(parameters):
    query_terms = {}
    ROW_LIMIT = 80
    for q in parameters['terms']:
        if q[1] != '*' and q[1] != '':
            query_terms[q[0]] = f"\"{q[1]}\""
        else:
            query_terms[q[0]] = q[1]
    try:
        start_row = ROW_LIMIT * (int(parameters['controls']['page']) - 1)
    except:
        start_row = 0
    result_fields = parameters['result_fields'] + [parmz.IMAGE_FIELD] + [parmz.TITLE_FIELD] + ['id']
    facet_fields = parameters['facet_fields']
    results = solr_query.solr_main_query(parameters['terms'], result_fields, facet_fields, ROW_LIMIT, start_row,
                                         parmz.FACET_LIMIT,
                                         parmz.FACET_MINCOUNT )
    full_facets = {}
    for f in results['facets']:
        if results['facets'][f] != {}:
            full_facets[f] = results['facets'][f]
    results['facets'] = full_facets
    results['start_row'] = start_row
    # for r in results['results']:
    #     for f in r:
    #         if type(r[f]) == type([]):
    #             r[f] = ', '.join(r[f])
    return results


VERSION = get_version()
