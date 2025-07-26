# holder for global variables and other parameters
class parmz:
    pass


# TODO: this needs a good deal of cleanup

parmz.TITLE = 'Blacklight MARC'
parmz.CITATION = 'Lowe, et al. 2025'
parmz.BANNER = 'Blacklight MARC'
parmz.LOGO = 'icon.svg'
parmz.BANNER_COLOR = 'black'
parmz.SECONDARY_COLOR = '#002868'
parmz.SOLR_CORE = 'blacklight-core'
parmz.SOLR_SERVER = 'http://localhost:8983'
parmz.FACET_LIMIT = 40
parmz.FACET_MINCOUNT = 1
parmz.ROW_LIMITS = [10, 20, 30]
parmz.TITLE_FIELD = 'title_tsim'
parmz.IMAGE_FIELD = 'IMAGES_ss'
parmz.IMAGE_DIRECTORY = 'images'
parmz.PORT = 3002

FIELD_DEFINITIONS = {}
parmz.SEARCH = [

]
FIELD_DEFINITIONS['SEARCH'] = parmz.SEARCH

parmz.FACETS = [
    ('Format', 'format'),
    ('Publication Year', 'pub_date_ssim'),
    ('Topic', 'subject_ssim'),
    ('Language', 'language_ssim'),
    ('Call Number', 'lc_1letter_ssim'),
    ('Region', 'subject_geo_ssim'),
    ('Era', 'subject_era_ssim'),
]
FIELD_DEFINITIONS['FACETS'] = parmz.FACETS
parmz.FACET_LABELS = {}
for f in parmz.FACETS:
    parmz.FACET_LABELS[f[1]] = f[0]

parmz.LIST = [

    ('Publish Date', 'example_query_facet_field'),
    ('Title', 'title_tsim'),
    ('Title', 'title_vern_ssim'),
    ('Author', 'author_tsim'),
    ('Author', 'author_vern_ssim'),
    ('Format', 'format'),
    ('Language', 'language_ssim'),
    ('Published', 'published_ssim'),
    ('Published', 'published_vern_ssim'),
    ('Call number', 'lc_callnum_ssim'),
]
FIELD_DEFINITIONS['LIST'] = parmz.LIST
FIELD_DEFINITIONS['TABLE'] = parmz.LIST

parmz.FULL = [
    ('Title', 'title_tsim'),
    ('Title', 'title_vern_ssim'),
    ('Subtitle', 'subtitle_tsim'),
    ('Subtitle', 'subtitle_vern_ssim'),
    ('Author', 'author_tsim'),
    ('Author', 'author_vern_ssim'),
    ('Format', 'format'),
    ('URL', 'url_fulltext_ssim'),
    ('More Information', 'url_suppl_ssim'),
    ('Language', 'language_ssim'),
    ('Published', 'published_ssim'),
    ('Published', 'published_vern_ssim'),
    ('Call number', 'lc_callnum_ssim'),
    ('ISBN', 'isbn_ssim'),
]

FIELD_DEFINITIONS['FULL'] = parmz.FULL

parmz.GALLERY = [
    ('Title', 'title_tsim'),
]
FIELD_DEFINITIONS['GALLERY'] = parmz.GALLERY

parmz.LAYOUTS = 'SEARCH FACETS LIST TABLE GALLERY FULL'.split(' ')
