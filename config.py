# holder for global variables and other parameters
class parmz:
    pass


# TODO: this needs a good deal of cleanup

parmz.TITLE = 'TAP'
parmz.CITATION = 'Lowe, et al. 2025'
parmz.BANNER = 'Thailand Archaeometallurgy Project'
parmz.LOGO = 'tap-logo-small.png'
parmz.BANNER_COLOR = '#EC5800'
parmz.SOLR_CORE = 'tap'
parmz.SOLR_SERVER = 'http://localhost:8983'
parmz.FACET_LIMIT = 40
parmz.FACET_MINCOUNT = 2
parmz.ROW_LIMITS = [10, 20, 30]
parmz.TITLE_FIELD = 'TITLE_s'
parmz.IMAGE_FIELD = 'IMAGES_ss'
parmz.PORT = 3002

FIELD_DEFINITIONS = {}
parmz.SEARCH = [
    ('Record types', 'DTYPES_ONLY_ss'),
    ('Site', 'SITE_s'),
    ('Op', 'OP_s'),
    ('Lot', 'LOT_s'),
    ('Level', 'LEVEL_s'),
    ('Area', 'AREA_s'),
    ('T no', 'T_s'),
    ('Year', 'YEAR_s'),
    ('Title', 'TITLE_s'),
    ('Key', 'KEY_s'),
    ('Entry date', 'ENTRY_DATE_s'),
    ('Registrar', 'REGISTRAR_s'),
    ('Excavator', 'EXCAVATOR_s'),
    ('Excavation date', 'EXCAVATION_DATE_s'),
    ('Count', 'COUNT_s'),
    ('Weight', 'WEIGHT_s'),
    ('Lab tray', 'LAB_TRAY_s'),
    ('Keyword', 'text'),
]
FIELD_DEFINITIONS['SEARCH'] = parmz.SEARCH

parmz.FACETS = [
    ('Record types', 'DTYPES_ONLY_ss'),
    ('Site', 'SITE_s'),
    ('Op', 'OP_s'),
    ('Lot', 'LOT_s'),
    ('Level', 'LEVEL_s'),
    ('Area', 'AREA_s'),
    ('T no', 'T_s'),
    ('Burial', 'BURIAL_s'),
    ('Year', 'YEAR_s'),
    ('Title', 'TITLE_s'),
    ('Key', 'KEY_s'),
    ('Entry date', 'ENTRY_DATE_s'),
    ('Registrar', 'REGISTRAR_s'),
    ('Excavator', 'EXCAVATOR_s'),
    ('Excavation date', 'EXCAVATION_DATE_s'),
    ('Count', 'COUNT_s'),
    ('Weight', 'WEIGHT_s'),
    ('Lab tray', 'LAB_TRAY_s'),
    ('Keyword', 'text'),
]
FIELD_DEFINITIONS['FACETS'] = parmz.FACETS
parmz.FACET_LABELS = {}
for f in parmz.FACETS:
    parmz.FACET_LABELS[f[1]] = f[0]

parmz.LIST = [
    ('Record types', 'DTYPES_ss'),
    ('Site', 'SITE_s'),
    ('Year', 'YEAR_s'),
    ('Op', 'OP_s'),
    ('Lot', 'LOT_s'),
    ('T no', 'T_s'),
    ('Burial', 'BURIAL_s'),
    ('Key', 'KEY_s'),
    # ('Title', 'TITLE_s'),
]
FIELD_DEFINITIONS['LIST'] = parmz.LIST

parmz.TABLE = [
    # ('Record types', 'DTYPES_ONLY_ss'),
    ('Site', 'SITE_s'),
    ('Year', 'YEAR_s'),
    ('Op', 'OP_s'),
    ('Lot', 'LOT_s'),
    ('Level', 'LEVEL_s'),
    ('Area', 'AREA_s'),
    ('T no', 'T_s'),
    ('Burial', 'BURIAL_s'),
    # ('Key', 'KEY_s'),
    ('Title', 'TITLE_s'),
]
FIELD_DEFINITIONS['TABLE'] = parmz.TABLE

parmz.FULL = [
    ('Record types', 'DTYPES_ss'),
    ('Site', 'SITE_s'),
    ('Op', 'OP_s'),
    ('Lot', 'LOT_s'),
    ('Level', 'LEVEL_s'),
    ('Area', 'AREA_s'),
    ('T no', 'T_s'),
    ('Burial', 'BURIAL_s'),
    ('Year', 'YEAR_s'),
    # ('Title', 'TITLE_s'),
    ('Key', 'KEY_s'),
    ('Entry date', 'ENTRY_DATE_s'),
    ('Registrar', 'REGISTRAR_s'),
    ('Excavator', 'EXCAVATOR_s'),
    ('Excavation date', 'EXCAVATION_DATE_s'),
    ('Count', 'COUNT_s'),
    ('Weight', 'WEIGHT_s'),
    ('Lab tray', 'LAB_TRAY_s'),
]
FIELD_DEFINITIONS['FULL'] = parmz.FULL

parmz.GALLERY = [
    # ('T no', 'T_s'),
    ('Title', 'TITLE_s'),
]
FIELD_DEFINITIONS['GALLERY'] = parmz.GALLERY

parmz.LAYOUTS = 'SEARCH FACETS LIST TABLE GALLERY FULL'.split(' ')
