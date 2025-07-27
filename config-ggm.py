# holder for global variables and other parameters
class parmz:
    pass


# TODO: this needs a good deal of cleanup

parmz.TITLE = 'Title'
parmz.CITATION = 'Lowe, et al. 2024'
parmz.BANNER = 'Gregory G. Maskarinec: Bāhās & Bahīs of Nepal'
parmz.BANNER_COLOR = '#EC5800'
parmz.SECONDARY_COLOR = '#002868'
parmz.LOGO = 'vajra.jpg'
parmz.SOLR_CORE = 'ggm'
parmz.SOLR_SERVER = 'http://localhost:8983'
parmz.FACET_LIMIT = 10
parmz.FACET_MINCOUNT = 2
parmz.ROW_LIMITS = [10, 20, 30]
parmz.IMAGE_FIELD = 'path_ss'
parmz.IMAGE_DIRECTORY = 'ggm-images'
parmz.TITLE_FIELD = 'title_s'
parmz.PORT = 3010

FIELD_DEFINITIONS = {}
parmz.SEARCH = [
    ('City', 'city_txt'),
    ('Year', 'year_txt'),
    ('Locke Number', 'lockenumber_txt'),
    ('Location', 'location_txt'),
    ('Title', 'title_txt')
]
FIELD_DEFINITIONS['SEARCH'] = parmz.SEARCH

parmz.FACETS = [
    ('City', 'city_s'),
    ('Year', 'year_s'),
    ('Day', 'day_of_month_s'),
    ('Locke Number', 'lockenumber_s'),
    ('Location', 'location_s'),
    ('Top Level', 'top_s'),
]
FIELD_DEFINITIONS['FACETS'] = parmz.FACETS
parmz.FACET_LABELS = {}
for f in parmz.FACETS:
    parmz.FACET_LABELS[f[1]] = f[0]

parmz.LIST = [
    ('City', 'city_s'),
    ('Year', 'year_s'),
    ('Day', 'day_of_month_s'),
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
    ('Day', 'day_of_month_s'),
    ('Locke Number', 'lockenumber_s'),
    ('Location', 'location_s'),
    ('Title', 'title_s'),
]
FIELD_DEFINITIONS['FULL'] = parmz.FULL

parmz.LAYOUTS = 'SEARCH FACETS LIST TABLE FULL'.split(' ')
