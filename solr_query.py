# autosuggest solr
#
# does NOT use the Solr4 "suggest" facility.
#
# instead, it uses facet queries.
#
# invoke as:
#
# http://localhost:8000/suggest/?q=1-200&elementID=ob.objno1
#
# returns json like:
#
# [{"value": "1-200"}, {"value": "1-20000"}, {"value": "1-200000"}, ...  {"value": "1-200025"}, {"s": "object"}]


# from django.http import HttpResponse
from config import parmz

import solr

# create a connection to a solr server
try:
    # create a connection to a solr server
    s = solr.SolrConnection(url='%s/solr/%s' % (parmz.SOLR_SERVER, parmz.SOLR_CORE))
except:
    print('could not open connection to "%s/solr/%s"' % (host, core))

import sys, json, re


def generate_solr_query(query_terms):
    pass


def solr_autosuggest(solr_field, solr_term, limit):
    # elapsedtime = time.time()

    try:
        query_field = solr_field.replace('_s', '_txt')
        # yes, case is a terrible thing to have to deal with!
        keyterms = [x for x in re.sub('[,\*+\.]', ' ', solr_term).lower().split(' ') if x != '']
        # make every token a left prefix...
        prefixes = [x + '*' for x in keyterms]
        query_string = ''
        for i, terms in enumerate(prefixes):
            query_string += f' AND ({query_field}:{prefixes[i]} OR {query_field}:{keyterms[i]})'
        query_string = query_string[4:]
        #        querystring = f'{solrField}:{solr_term}*'
        response = s.query(query_string, facet='true', facet_field=[solr_field.replace('_txt', '_s')], fq={},
                           rows=0, facet_limit=limit,
                           facet_mincount=1)

        facets = response.facet_counts['facet_fields']
        result = []
        for key, values in facets.items():
            for k, v in values.items():
                result.append(k)

        result = sorted(result, key=lambda v: v.upper())

        # return suggested in alphabetical order (case insensitive)
        return json.dumps(result)

    except:
        sys.stderr.write("suggest solr query error!\n")
        return None


def solr_main_query(query_terms, result_fields, facet_fields, row_limit, start_row, facet_limit, facet_mincount):
    query_string = ' AND '.join(f'{q}:{query_terms[q]}' for q in query_terms)
    response = s.query(query_string, facet='true', facet_field=[f.replace('_txt', '_s') for f in facet_fields],
                       fq={},
                       fields=result_fields,
                       rows=row_limit, start=start_row, facet_limit=facet_limit,
                       facet_mincount=facet_mincount)

    facets = response.facet_counts['facet_fields']
    result = {'facets': facets, 'results': response.results, 'query': query_string, 'terms': query_terms,
              'numfound': response.numFound}
    return result


if __name__ == '__main__':
    print(solr_autosuggest('lockenumber_s', 'K2', 10))

    query_terms = {'lockenumber_txt': 'K2*', 'year_s': '2010'}
    result_fields = ('lockenumber_s', 'year_s')
    facet_fields = ('year_s', 'location_s')
    print(solr_main_query(query_terms, result_fields, facet_fields, 10, 5))
