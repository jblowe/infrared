# holder for global variables and other parameters
class parmz:
    pass


# TODO: this needs a good deal of cleanup

parmz.TITLE = 'TAP'
parmz.CITATION = 'Lowe, et al. 2025'
parmz.BANNER = 'Thailand Archaeometallurgy Project'
parmz.LOGO = 'tap-logo-small.svg'
parmz.BANNER_COLOR = '#A51931'
parmz.SECONDARY_COLOR = '#002868'
parmz.NAVBAR = 'navbar-dark'
parmz.SOLR_CORE = 'tap'
parmz.SOLR_SERVER = 'http://localhost:8983'
parmz.FACET_LIMIT = 40
parmz.FACET_MINCOUNT = 1
parmz.ROW_LIMITS = [10, 20, 30]
parmz.TITLE_FIELD = 'TITLE_ss'
parmz.IMAGE_FIELD = 'THUMBNAIL_ss'
parmz.IMAGE_PREFIX = '/images'
parmz.PORT = 3002

FIELD_DEFINITIONS = {}
parmz.SEARCH = [
    ('Record types', 'DTYPE_ss'),
    ('Site', 'SITE_txt'),
    ('Op', 'OP_txt'),
    ('Lot', 'LOT_txt'),
    ('Level', 'LEVEL_txt'),
    ('Area', 'AREA_txt'),
    ('T no', 'T_txt'),
    ('Year', 'YEAR_txt'),
    ('Title', 'TITLE_txt'),
    ('Key', 'KEY_txt'),
    ('Entry date', 'ENTRY_DATE_txt'),
    ('Registrar', 'REGISTRAR_txt'),
    ('Excavator', 'EXCAVATOR_txt'),
    ('Excavation date', 'EXCAVATION_DATE_txt'),
    ('Count', 'COUNT_txt'),
    ('Weight', 'WEIGHT_txt'),
    ('Penn Inventory', 'TRAY_txt'),
    ('Keyword', 'text'),
]
FIELD_DEFINITIONS['SEARCH'] = parmz.SEARCH

parmz.FACETS = [
    ('Record types', 'DTYPE_ss'),
    ('Site', 'SITE_ss'),
    ('Year', 'YEAR_ss'),
    ('Op', 'OP_ss'),
    ('Lot', 'LOT_ss'),
    ('Level', 'LEVEL_ss'),
    ('Area', 'AREA_ss'),
    ('T no', 'T_ss'),
    ('Burial', 'BURIAL_ss'),
    # ('Season', 'SEASON_ss'),
    ('Title', 'TITLE_ss'),
    ('Document kind', 'DOC_ss'),
    ('Key', 'KEY_ss'),
    ('Entry date', 'ENTRY_DATE_ss'),
    ('Registrar', 'REGISTRAR_ss'),
    ('Excavator', 'EXCAVATOR_ss'),
    ('Excavation date', 'EXCAVATION_DATE_ss'),
    ('Count', 'COUNT_ss'),
    ('Weight', 'WEIGHT_ss'),
    ('Penn Inventory', 'TRAY_ss'),
    ('Keyword', 'text'),
]
FIELD_DEFINITIONS['FACETS'] = parmz.FACETS
parmz.FACET_LABELS = {}
for f in parmz.FACETS:
    parmz.FACET_LABELS[f[1]] = f[0]

# add the labels for search, too
for f in parmz.SEARCH:
    parmz.FACET_LABELS[f[1]] = f[0]

parmz.LIST = [
    ('Record types', 'DTYPE_ss'),
    ('T no', 'T_ss'),
    ('Site', 'SITE_ss'),
    ('Year', 'YEAR_ss'),
    ('Op', 'OP_ss'),
    ('Lot', 'LOT_ss'),
    ('Burial', 'BURIAL_ss'),
    ('Key', 'KEY_ss'),
    # ('Title', 'TITLE_ss'),
]
FIELD_DEFINITIONS['LIST'] = parmz.LIST

parmz.TABLE = [
    # ('Record types', 'DTYPE_ss'),
    ('T no', 'T_ss'),
    ('Site', 'SITE_ss'),
    ('Year', 'YEAR_ss'),
    # ('Season', 'SEASON_ss'),
    ('Op', 'OP_ss'),
    ('Area', 'AREA_ss'),
    ('Lot', 'LOT_ss'),
    ('Level', 'LEVEL_ss'),
    ('Burial', 'BURIAL_ss'),
    ('Feature', 'FEA_ss'),
    # ('Key', 'KEY_ss'),
    ('Title', 'TITLE_ss'),
]
FIELD_DEFINITIONS['TABLE'] = parmz.TABLE

parmz.FULL = [
    ('Record types', 'DTYPE_ss'),
    ('Site', 'SITE_ss'),
    ('Op', 'OP_ss'),
    ('Sq', 'SQ_ss'),
    ('Lot', 'LOT_ss'),
    ('Level', 'LEVEL_ss'),
    ('Area', 'AREA_ss'),
    ('T no', 'T_ss'),
    ('Burial', 'BURIAL_ss'),
    ('Year', 'YEAR_ss'),
    ('Season', 'SEASON_ss'),
    # ('Title', 'TITLE_ss'),
    # ('Key', 'KEY_ss'),
    ('Entry date', 'ENTRY_DATE_ss'),
    ('Registrar', 'REGISTRAR_ss'),
    ('Excavator', 'EXCAVATOR_ss'),
    ('Excavation date', 'EXCAVATION_DATE_ss'),
    ('Count', 'COUNT_ss'),
    ('Weight', 'WEIGHT_ss'),
    ('Penn Inventory', 'TRAY_ss'),
    # ('DTYPE', 'DTYPE_ss'),
    # ('Records', 'RECORDS_ss'),
    # ('Images', 'IMAGES_ss'),
    # ('Filenames', 'FILENAMES_ss'),
    ('Roll', 'ROLL_ss'),
    ('Exp', 'EXP_ss'),
    ('Material', 'MATERIAL_ss'),
    ('Notes', 'NOTES_ss'),
    ('Stratum', 'STRATUM_ss'),
    ('Class', 'CLASS_ss'),
    # ('Image name', 'IMAGENAME_ss'),
    # ('Filename', 'FILENAME_ss'),
    ('Count', 'COUNT_ss'),
    ('Directory', 'DIRECTORY_ss'),
    # ('DTYPE', 'DTYPE_ss'),
    ('Entry', 'ENTRY_DATE_ss'),
    ('Etc', 'ETC_ss'),
    ('Feature', 'FEA_ss'),
    # ('Filenames', 'FILENAMES_ss'),
    # ('Images', 'IMAGES_ss'),
    ('Keyterms', 'KEYTERMS_ss'),
    # ('Records', 'RECORDS_ss'),
    ('Reg no', 'REG_ss'),
    ('Object no', 'OBJ_ss'),
    ('Unknown', 'UNKNOWN_ss'),
    ('Weight', 'WEIGHT_ss'),
    ('Title', 'TITLE_ss'),
    ('Document kind', 'DOC_ss'),
]
FIELD_DEFINITIONS['FULL'] = parmz.FULL

parmz.GALLERY = [
    # ('T no', 'T_ss'),
    ('Title', 'TITLE_ss'),
]
FIELD_DEFINITIONS['GALLERY'] = parmz.GALLERY

parmz.LAYOUTS = 'SEARCH FACETS LIST TABLE GALLERY FULL'.split(' ')
