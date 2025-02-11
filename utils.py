import os, time, sys
import lxml.etree as ET

from bottle import template

from config import *
import solr_query

# nb: we are trying to get the directory above the directory this file is in
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_version():
    return ''
    try:
        with os.popen("/usr/bin/git describe --always") as f:
            version = f.read().strip()
        if version == '':  # try alternate location for git (this is the usual Mac location)
            with os.popen("/usr/local/bin/git describe --always") as f:
                version = f.read().strip()
    except:
        version = 'Unknown'
    return version


def add_time_and_version():
    return 'code and data version: %s, system last restarted: %s' % (
        get_version(), time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))


def check_template(tpl, data, parameters):
    if 'back' not in data:
        data['back'] = '/'
    return template(tpl, data=data)


def query(parameters):
    query_terms = parameters['terms']
    for q in query_terms:
        if q != '*':
            query_terms[q] = f'"{query_terms[q]}"'
    result_fields = parameters['result_fields']
    facet_fields = parameters['facet_fields']
    row_limit = 10
    facet_limit = 5
    results = solr_query.solr_main_query(query_terms, result_fields, facet_fields, row_limit, facet_limit)
    return results


VERSION = get_version()
