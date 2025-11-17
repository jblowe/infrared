# holder for global variables and other parameters
class parmz:
    pass


# TODO: this needs a good deal of cleanup

parmz.TITLE = 'MMAP'
parmz.CITATION = 'mmap project'
parmz.BANNER = 'Middle Mekong Archaeology Project'
parmz.BANNER_COLOR = '#f9d88d'
parmz.SECONDARY_COLOR = '#002868'
parmz.NAVBAR = 'navbar-light'
parmz.LOGO = 'mmap-logo-pot-and-river.png'
parmz.SOLR_CORE = 'laos'
parmz.SOLR_SERVER = 'http://localhost:8983'
parmz.FACET_LIMIT = 100
parmz.FACET_MINCOUNT = 2
parmz.ROW_LIMITS = [10, 20, 30]
parmz.IMAGE_FIELD = 'THUMBNAIL_ss'
parmz.IMAGE_PREFIX = '/mmap-images'
parmz.TITLE_FIELD = 'SITE_s'
parmz.PORT = 3011

FIELD_DEFINITIONS = {}

parmz.SEARCH = [
    ('ID', 'mmap_artifact_id_txt'),
    ('Site Name', 'SITE_txt'),
    ('Date Discovered', 'DATE_txt'),
    ('Type', 'TYPE_s'),
]
FIELD_DEFINITIONS['SEARCH'] = parmz.SEARCH

parmz.FACETS = [
    ('Site Name', 'SITE_s'),
    ('Date Discovered', 'DATE_s'),
    ('Type', 'TYPE_s'),
]

parmz.LIST = [
    ('Artifact ID', 'mmap_artifact_id_s'),
    ('Site Name', 'SITE_s'),
    ('Date Discovered', 'DATE_s'),
    ('Type', 'TYPE_s'),
]
FIELD_DEFINITIONS['LIST'] = parmz.LIST

parmz.TABLE = [
    ('Artifact ID', 'mmap_artifact_id_s'),
    ('Site Name', 'SITE_s'),
    ('Type', 'TYPE_s'),
    ('Bag ID', 'TYPE_txt'),
    ('Image', 'THUMBNAIL_s'),
]
FIELD_DEFINITIONS['TABLE'] = parmz.TABLE

parmz.GALLERY = [
    ('Artifact ID', 'mmap_artifact_id_s'),
    ('Site Name', 'SITE_s'),
    ('Type', 'TYPE_s'),
]
FIELD_DEFINITIONS['GALLERY'] = parmz.GALLERY

parmz.FULL = [
    ('Artifact ID', 'mmap_artifact_id_s'),
    ('Site Name', 'SITE_s'),
    ('Date Discovered', 'DATE_s'),
    ('Type', 'TYPE_s'),
]
FIELD_DEFINITIONS['FULL'] = parmz.FULL

FIELD_DEFINITIONS['FACETS'] = parmz.FACETS
parmz.FACET_LABELS = {}
for f in parmz.FACETS:
    parmz.FACET_LABELS[f[1]] = f[0]

parmz.LAYOUTS = 'SEARCH FACETS LIST TABLE GALLERY FULL'.split(' ')

