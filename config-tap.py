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
parmz.TITLE_FIELD = 'TITLE_s'
parmz.IMAGE_FIELD = 'IMAGES_ss'
parmz.IMAGE_DIRECTORY = 'images'
parmz.PORT = 3002

FIELD_DEFINITIONS = {}
parmz.SEARCH = [
    ('Record types', 'DTYPES_ONLY_ss'),
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
    ('Record types', 'DTYPES_ONLY_ss'),
    ('Site', 'SITE_s'),
    ('Year', 'YEAR_s'),
    ('Op', 'OP_s'),
    ('Lot', 'LOT_s'),
    ('Level', 'LEVEL_s'),
    ('Area', 'AREA_s'),
    ('T no', 'T_s'),
    ('Burial', 'BURIAL_s'),
    # ('Season', 'SEASON_s'),
    ('Title', 'TITLE_s'),
    ('Document kind', 'DOC_ss'),
    ('Key', 'KEY_s'),
    ('Entry date', 'ENTRY_DATE_s'),
    ('Registrar', 'REGISTRAR_s'),
    ('Excavator', 'EXCAVATOR_s'),
    ('Excavation date', 'EXCAVATION_DATE_s'),
    ('Count', 'COUNT_s'),
    ('Weight', 'WEIGHT_s'),
    ('Penn Inventory', 'TRAY_s'),
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
    ('Record types', 'DTYPES_ss'),
    ('T no', 'T_s'),
    ('Site', 'SITE_s'),
    ('Year', 'YEAR_s'),
    ('Op', 'OP_s'),
    ('Lot', 'LOT_s'),
    ('Burial', 'BURIAL_s'),
    ('Key', 'KEY_s'),
    # ('Title', 'TITLE_s'),
]
FIELD_DEFINITIONS['LIST'] = parmz.LIST

parmz.TABLE = [
    # ('Record types', 'DTYPES_ONLY_ss'),
    ('T no', 'T_s'),
    ('Site', 'SITE_s'),
    ('Year', 'YEAR_s'),
    # ('Season', 'SEASON_s'),
    ('Op', 'OP_s'),
    ('Area', 'AREA_s'),
    ('Lot', 'LOT_s'),
    ('Level', 'LEVEL_s'),
    ('Burial', 'BURIAL_s'),
    ('Feature', 'FEA_s'),
    # ('Key', 'KEY_s'),
    ('Title', 'TITLE_s'),
]
FIELD_DEFINITIONS['TABLE'] = parmz.TABLE

parmz.FULL = [
    ('Record types', 'DTYPES_ss'),
    ('Site', 'SITE_s'),
    ('Op', 'OP_s'),
    ('Sq', 'SQ_s'),
    ('Lot', 'LOT_s'),
    ('Level', 'LEVEL_s'),
    ('Area', 'AREA_s'),
    ('T no', 'T_s'),
    ('Burial', 'BURIAL_s'),
    ('Year', 'YEAR_s'),
    ('Season', 'SEASON_s'),
    # ('Title', 'TITLE_s'),
    # ('Key', 'KEY_s'),
    ('Entry date', 'ENTRY_DATE_s'),
    ('Registrar', 'REGISTRAR_s'),
    ('Excavator', 'EXCAVATOR_s'),
    ('Excavation date', 'EXCAVATION_DATE_s'),
    ('Count', 'COUNT_s'),
    ('Weight', 'WEIGHT_s'),
    ('Penn Inventory', 'TRAY_s'),
    # ('Dtypes', 'DTYPES_ONLY_ss'),
    # ('Records', 'RECORDS_ss'),
    # ('Images', 'IMAGES_ss'),
    # ('Filenames', 'FILENAMES_ss'),
    ('Roll', 'ROLL_s'),
    ('Exp', 'EXP_s'),
    ('Material', 'MATERIAL_s'),
    ('Notes', 'NOTES_s'),
    ('Stratum', 'STRATUM_s'),
    ('Class', 'CLASS_s'),
    # ('Image name', 'IMAGENAME_s'),
    # ('Filename', 'FILENAME_s'),
    ('Count', 'COUNT_s'),
    ('Directory', 'DIRECTORY_s'),
    # ('Dtypes', 'DTYPES_ONLY_ss'),
    ('Entry', 'ENTRY_DATE_s'),
    ('Etc', 'ETC_s'),
    ('Feature', 'FEA_s'),
    # ('Filenames', 'FILENAMES_ss'),
    # ('Images', 'IMAGES_ss'),
    ('Keyterms', 'KEYTERMS_ss'),
    # ('Records', 'RECORDS_ss'),
    ('Reg no', 'REG_s'),
    ('Object no', 'OBJ_s'),
    ('Unknown', 'UNKNOWN_s'),
    ('Weight', 'WEIGHT_s'),
    ('Title', 'TITLE_s'),
    ('Document kind', 'DOC_ss'),
]
FIELD_DEFINITIONS['FULL'] = parmz.FULL

parmz.GALLERY = [
    # ('T no', 'T_s'),
    ('Title', 'TITLE_s'),
]
FIELD_DEFINITIONS['GALLERY'] = parmz.GALLERY

parmz.LAYOUTS = 'SEARCH FACETS LIST TABLE GALLERY FULL'.split(' ')
