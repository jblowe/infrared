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
parmz.SOLR_CORE = 'mmap-public'
parmz.SOLR_SERVER = 'http://localhost:8983'
parmz.FACET_LIMIT = 100
parmz.FACET_MINCOUNT = 2
parmz.ROW_LIMITS = [10, 20, 30]
parmz.IMAGE_FIELD = 'images_ss'
parmz.IMAGE_PREFIX = '/mmap-qdrive'
parmz.TITLE_FIELD = 'mmap_artifact_id_s'
parmz.PORT = 3011

FIELD_DEFINITIONS = {}

parmz.SEARCH = [
    ('Artifact ID', 'mmap_artifact_id_txt'),
    ('Site Name', 'site_name_txt'),
    ('Date Discovered', 'date_discovered_txt'),
    ('Bag ID', 'bag_id_txt'),
    ('Artifact Condition', 'artifact_condition_txt'),
    ('Artifact Class', 'artifact_class_txt'),
    ('Maximum Dimension', 'maximum_dimension_txt'),
    ('Weight', 'weight_txt'),
    ('Count', 'count_txt'),
    ('Burial No', 'burial_no_txt'),
    ('Period', 'period_txt'),
    ('Material', 'material_txt'),
    ('Comments', 'comments_txt'),
    ('Bur Phase', 'bur_phase_txt'),
    ('Level', 'level_txt'),
    ('Depcontext', 'depcontext_txt'),
    ('Square', 'square_txt'),
    ('Quad', 'quad_txt'),
    ('Layer', 'layer_txt'),
    ('Feano', 'feano_txt'),
    ('Featype', 'featype_txt'),
    ('Burassoc', 'burassoc_txt'),
    ('Blocation', 'blocation_txt'),
    ('Bodypart', 'bodypart_txt'),
    ('Sherdample? S', 'sherd_txtample?_txt'),
    ('Sherdamp Location S', 'sherd_txtamp_location_txt'),
    ('Thinection S', 'thin_txtection_txt'),
    ('Ts Location', 'ts_location_txt'),
    ('Ts No', 'ts_no_txt'),
    ('Met sample S', 'met_sample_txt'),
    ('Met samp Loc S', 'met_samp_loc_txt'),
    ('Sample Comment', 'sample_comment_txt'),
    ('Artloc', 'artloc_txt'),
    ('Conserved', 'conserved_txt'),
    ('Glass sample S', 'glass_sample_txt'),
    ('Gl samp S', 'gl_samp_txt'),
    ('Gl Tech', 'gl_tech_txt'),
    ('Gl Analy Date', 'gl_analy_date_txt'),
    ('Entered By', 'entered_by_txt'),
    ('Initial Date', 'initial_date_txt'),
    ('Date Last Modified', 'date_last_modified_txt'),
    # ('Txtimagename1', 'txtimagename1_txt'),
    # ('Txtimagename2', 'txtimagename2_txt'),
    # ('Txtimagename3', 'txtimagename3_txt'),
    # ('Txtimagename4', 'txtimagename4_txt'),
    # ('Txtimagename5', 'txtimagename5_txt'),
    # ('Txtdrawingname', 'txtdrawingname_txt'),
]
FIELD_DEFINITIONS['SEARCH'] = parmz.SEARCH

parmz.FACETS = [
    ('Site Name', 'site_name_s'),
    ('Date Discovered', 'date_discovered_s'),
    ('Bag ID', 'bag_id_s'),
    ('Artifact Class', 'artifact_class_s'),
    ('Period', 'period_s'),
    ('Material', 'material_s'),
    ('Bur Phase', 'bur_phase_s'),
    ('Level', 'level_s'),
    ('Square', 'square_s'),
    ('Quad', 'quad_s'),
    ('Layer', 'layer_s'),
    ('Feano', 'feano_s'),
    ('Featype', 'featype_s'),
    ('Flag For Check', 'flag_for_check_s')
]

parmz.LIST = [
    ('Artifact ID', 'mmap_artifact_id_s'),
    ('Site Name', 'site_name_s'),
    ('Date Discovered', 'date_discovered_s'),
    ('Bag ID', 'bag_id_s'),
    ('Artifact Condition', 'artifact_condition_s'),
    ('Artifact Class', 'artifact_class_s'),
    ('Maximum Dimension', 'maximum_dimension_s'),
    ('Weight', 'weight_s'),
    ('Count', 'count_s'),
    ('Burial No', 'burial_no_s'),
    ('Period', 'period_s'),
    ('Material', 'material_s'),
    ('Comments', 'comments_s'),
    ('Bur Phase', 'bur_phase_s'),
    ('Level', 'level_s'),
    ('Depcontext', 'depcontext_s'),
    ('Square', 'square_s'),
    ('Quad', 'quad_s'),
    ('Layer', 'layer_s'),
    ('Feano', 'feano_s'),
    ('Featype', 'featype_s'),
    ('Burassoc', 'burassoc_s'),
    ('Blocation', 'blocation_s'),
    ('Bodypart', 'bodypart_s'),
    ('Sherdample? S', 'sherd_sample?_s'),
    ('Sherdamp Location S', 'sherd_samp_location_s'),
    ('Thinection S', 'thin_section_s'),
    ('Ts Location', 'ts_location_s'),
    ('Ts No', 'ts_no_s'),
    ('Met sample S', 'met_sample_s'),
    ('Met samp Loc S', 'met_samp_loc_s'),
    ('Sample Comment', 'sample_comment_s'),
    ('Artloc', 'artloc_s'),
    ('Conserved', 'conserved_s'),
    ('Glass sample S', 'glass_sample_s'),
    ('Glamp S', 'gl_samp_s'),
    ('Gl Tech', 'gl_tech_s'),
    ('Gl Analy Date', 'gl_analy_date_s'),
    ('Entered By', 'entered_by_s'),
    ('Initial Date', 'initial_date_s'),
    ('Date Last Modified', 'date_last_modified_s'),
    # ('Txtimagename1', 'txtimagename1_s'),
    # ('Txtimagename2', 'txtimagename2_s'),
    # ('Txtimagename3', 'txtimagename3_s'),
    # ('Txtimagename4', 'txtimagename4_s'),
    # ('Txtimagename5', 'txtimagename5_s'),
    # ('Txtdrawingname', 'txtdrawingname_s'),
    ('Flag For Check', 'flag_for_check_s'),
]
FIELD_DEFINITIONS['LIST'] = parmz.LIST

parmz.TABLE = [
    ('Artifact ID', 'mmap_artifact_id_s'),
    ('Site Name', 'site_name_s'),
    # ('Bag ID', 'bag_id_s'),
    ('Artifact Class', 'artifact_class_s'),
    ('Max. Dim', 'maximum_dimension_s'),
    ('Weight', 'weight_s'),
    ('Count', 'count_s'),
    ('Burial No', 'burial_no_s'),
    ('Period', 'period_s'),
    ('Material', 'material_s'),
    ('Level', 'level_s'),
    ('Square', 'square_s'),
    ('Quad', 'quad_s'),
    ('Layer', 'layer_s'),
]
FIELD_DEFINITIONS['TABLE'] = parmz.TABLE

parmz.GALLERY = [
    ('Artifact ID', 'mmap_artifact_id_s'),
    ('Site Name', 'site_name_s'),
    ('Artifact Class', 'artifact_class_s'),
]
FIELD_DEFINITIONS['GALLERY'] = parmz.GALLERY

parmz.FULL = [
    ('Artifact ID', 'mmap_artifact_id_s'),
    ('Site Name', 'site_name_s'),
    ('Date Discovered', 'date_discovered_s'),
    ('Bag ID', 'bag_id_s'),
    ('Artifact Condition', 'artifact_condition_s'),
    ('Artifact Class', 'artifact_class_s'),
    ('Maximum Dimension', 'maximum_dimension_s'),
    ('Weight', 'weight_s'),
    ('Count', 'count_s'),
    ('Burial No', 'burial_no_s'),
    ('Period', 'period_s'),
    ('Material', 'material_s'),
    ('Comments', 'comments_s'),
    ('Bur Phase', 'bur_phase_s'),
    ('Level', 'level_s'),
    ('Depcontext', 'depcontext_s'),
    ('Square', 'square_s'),
    ('Quad', 'quad_s'),
    ('Layer', 'layer_s'),
    ('Feano', 'feano_s'),
    ('Featype', 'featype_s'),
    ('Burassoc', 'burassoc_s'),
    ('Blocation', 'blocation_s'),
    ('Bodypart', 'bodypart_s'),
    ('Sherdample? S', 'sherd_sample?_s'),
    ('Sherdamp Location S', 'sherd_samp_location_s'),
    ('Thinection S', 'thin_section_s'),
    ('Ts Location', 'ts_location_s'),
    ('Ts No', 'ts_no_s'),
    ('Met sample S', 'met_sample_s'),
    ('Met samp Loc S', 'met_samp_loc_s'),
    ('Sample Comment', 'sample_comment_s'),
    ('Artloc', 'artloc_s'),
    ('Conserved', 'conserved_s'),
    ('Glass sample S', 'glass_sample_s'),
    ('Glamp S', 'gl_samp_s'),
    ('Gl Tech', 'gl_tech_s'),
    ('Gl Analy Date', 'gl_analy_date_s'),
    ('Entered By', 'entered_by_s'),
    ('Initial Date', 'initial_date_s'),
    ('Date Last Modified', 'date_last_modified_s'),
    # ('Txtimagename1', 'txtimagename1_s'),
    # ('Txtimagename2', 'txtimagename2_s'),
    # ('Txtimagename3', 'txtimagename3_s'),
    # ('Txtimagename4', 'txtimagename4_s'),
    # ('Txtimagename5', 'txtimagename5_s'),
    # ('Txtdrawingname', 'txtdrawingname_s'),
    ('Flag For Check', 'flag_for_check_s'),
]
FIELD_DEFINITIONS['FULL'] = parmz.FULL

FIELD_DEFINITIONS['FACETS'] = parmz.FACETS
parmz.FACET_LABELS = {}
for f in parmz.FACETS:
    parmz.FACET_LABELS[f[1]] = f[0]

parmz.LAYOUTS = 'SEARCH FACETS LIST TABLE GALLERY FULL'.split(' ')

