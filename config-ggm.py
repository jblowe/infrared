# holder for global variables and other parameters
class parmz:
    pass


# TODO: this needs a good deal of cleanup

parmz.TITLE = 'Title'
parmz.CITATION = 'Lowe, et al. 2024'
parmz.BANNER = 'Infrared Search Engine'
parmz.BANNER_COLOR = '#EC5800'
parmz.SOLR_CORE = 'ggm'
parmz.SOLR_SERVER = 'http://localhost:8983'
parmz.FACET_LIMIT = 10
parmz.FACET_MINCOUNT = 2
parmz.ROW_LIMITS = [10, 20, 30]
parmz.IMAGE_FIELD = 'path_s'
parmz.TITLE_FIELD = 'title_s'
parmz.PORT = 3010

parmz.title = 'Title'
parmz.citation = 'Lowe, et al. 2024'
parmz.banner = 'Infrared Search Engine'
parmz.banner_color = '#EC5800'
parmz.solr_core = 'ggm'
parmz.solr_server = 'http://localhost:8983'
parmz.facet_limits = 10
parmz.row_limits = [10, 20, 30]

FIELD_DEFINITIONS = {}
parmz.SEARCH = [
    ('City', 'city_s'),
    ('Year', 'year_s'),
    ('Locke Number', 'lockenumber_s'),
    ('Location', 'location_s'),
    ('Title', 'title_s')
]
FIELD_DEFINITIONS['SEARCH'] = parmz.SEARCH

parmz.FACETS = [
    ('City', 'city_s'),
    ('Year', 'year_s'),
    ('Locke Number', 'lockenumber_s'),
    ('Location', 'location_s'),
]
FIELD_DEFINITIONS['FACETS'] = parmz.FACETS
parmz.FACET_LABELS = {}
for f in parmz.FACETS:
    parmz.FACET_LABELS[f[1]] = f[0]

parmz.LIST = [
    ('City', 'city_s'),
    ('Year', 'year_s'),
    ('Locke Number', 'lockenumber_s'),
    ('Location', 'location_s'),
    ('Title', 'title_s'),
]
FIELD_DEFINITIONS['LIST'] = parmz.LIST

parmz.TABLE = [
    ('City', 'city_s'),
    ('Year', 'year_s'),
    ('Locke Number', 'lockenumber_s'),
    ('Location', 'location_s'),
    ('Title', 'title_s'),
]
FIELD_DEFINITIONS['TABLE'] = parmz.TABLE

parmz.GALLERY = [
    ('Title', 'title_s'),
]

FIELD_DEFINITIONS['GALLERY'] = parmz.GALLERY

parmz.FULL = [
    ('City', 'city_s'),
    ('Year', 'year_s'),
    ('Locke Number', 'lockenumber_s'),
    ('Location', 'location_s'),
    ('Title', 'title_s'),
]
FIELD_DEFINITIONS['FULL'] = parmz.FULL

parmz.LAYOUTS = 'SEARCH FACETS LIST TABLE FULL'.split(' ')
