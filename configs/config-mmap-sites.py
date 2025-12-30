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
parmz.SOLR_CORE = 'mmap-sites'
parmz.SOLR_SERVER = 'http://localhost:8983'
parmz.FACET_LIMIT = 100
parmz.FACET_MINCOUNT = 2
parmz.ROW_LIMITS = [10, 20, 30]
parmz.IMAGE_FIELD = 'General_view_THUMBNAILS_ss'
parmz.IMAGE_PREFIX = '/mmap-images'
parmz.TITLE_FIELD = 'site_name_s'
parmz.PORT = 3011

FIELD_DEFINITIONS = {}

parmz.SEARCH = [
    ('ID', 'siteid_s'),
    ('Site Name', 'site_name_txt'),
    ('Date Discovered', 'site_date_s')
]
FIELD_DEFINITIONS['SEARCH'] = parmz.SEARCH

parmz.FACETS = [
    ('site name', 'site_name_s'),
    ('short site name', 'site_short_s'),
    ('site date', 'site_date_s'),
    ('gis code', 'gis_code_s'),
    ('env contxt', 'env_contxt_s'),
    ('access', 'acces_s'),
    ('vill name', 'vill_name_s'),
    ('village id', 'village_id_s'),
    ('nrprimrv', 'nrprimrv_s'),
    ('nrsecrv', 'nrsecrv_s'),
    ('dimena', 'dimena_s'),
    ('dimaorient', 'dimaorient_s'),
    ('dimenb', 'dimenb_s'),
    ('dimborient', 'dimborient_s'),
    ('estdepth', 'estdepth_s'),
    ('exc pri', 'exc_pri_s'),
    ('point y', 'point_y_s'),
    ('point x', 'point_x_s'),
    ('site characteristics', 'site_characteristics_s'),
    ('site comm', 'site_comm_s'),
    ('site conditions', 'site_conditions_s'),
    ('cvmthht', 'cvmthht_s'),
    ('cave fl', 'cave_fl_s'),
    ('cvmthdir', 'cvmthdir_s'),
    ('cavemoist', 'cavemoist_s'),
    ('artdens', 'artdens_s'),
    ('condcomm', 'condcomm_s'),
    ('recent disturbance', 'recent_disturbance_s'),
    ('distcomm', 'distcomm_s'),
    ('pastite functions_s', 'past_site_functions_s'),
    ('pastfcomm', 'pastfcomm_s'),
    ('environment', 'environment_s'),
    ('natveg', 'natveg_s'),
    ('crops', 'crops_s'),
    ('wldedpl', 'wldedpl_s'),
    ('indplant', 'indplant_s'),
    ('fauna', 'fauna_s'),
    ('envcomm', 'envcomm_s'),
    ('artifacts present', 'artifacts_present_s'),
    ('oth art', 'oth_art_s'),
    ('artcomm', 'artcomm_s'),
    ('image info', 'image_info_s'),
    ('imagenos', 'imagenos_s'),
    ('txtimagename1', 'txtimagename1_s'),
    ('imagecomm', 'imagecomm_s'),
    ('sitedesc', 'sitedesc_s'),
    ('river team', 'river_team_s'),
    ('timepent_s', 'time_spent_s'),
    ('entered by', 'entered_by_s'),
    ('initial date', 'initial_date_s'),
    ('last modified', 'last_modified_s'),
    ('visit comm', 'visit_comm_s')
]

parmz.LIST = [
    ('id', 'id'),
    ('siteid', 'siteid_s'),
    ('site num', 'site_num_s'),
    ('site name', 'site_name_s'),
    ('short site name', 'site_short_s'),
    ('site date', 'site_date_s'),
    ('year recorded', 'year_recorded_s'),
    ('gis code', 'gis_code_s'),
    ('env contxt', 'env_contxt_s'),
    ('access', 'acces_s'),
    ('vill name', 'vill_name_s'),
    ('village id', 'village_id_s'),
    ('nrprimrv', 'nrprimrv_s'),
    ('nrsecrv', 'nrsecrv_s'),
    ('dimena', 'dimena_s'),
    ('dimaorient', 'dimaorient_s'),
    ('dimenb', 'dimenb_s'),
    ('dimborient', 'dimborient_s'),
    ('estdepth', 'estdepth_s'),
    ('exc pri', 'exc_pri_s'),
    ('point y', 'point_y_s'),
    ('point x', 'point_x_s'),
    ('utm x', 'utm_x_s'),
    ('utm y', 'utm_y_s'),
    ('site characteristics', 'site_characteristics_s'),
    ('site comm', 'site_comm_s'),
    ('site conditions', 'site_conditions_s'),
    ('cvmthht', 'cvmthht_s'),
    ('cave fl', 'cave_fl_s'),
    ('cvmthdir', 'cvmthdir_s'),
    ('cavemoist', 'cavemoist_s'),
    ('artdens', 'artdens_s'),
    ('condcomm', 'condcomm_s'),
    ('recent disturbance', 'recent_disturbance_s'),
    ('distcomm', 'distcomm_s'),
    ('pastite functions_s', 'past_site_functions_s'),
    ('pastfcomm', 'pastfcomm_s'),
    ('environment', 'environment_s'),
    ('natveg', 'natveg_s'),
    ('crops', 'crops_s'),
    ('wldedpl', 'wldedpl_s'),
    ('indplant', 'indplant_s'),
    ('fauna', 'fauna_s'),
    ('envcomm', 'envcomm_s'),
    ('artifacts present', 'artifacts_present_s'),
    ('oth art', 'oth_art_s'),
    ('artcomm', 'artcomm_s'),
    ('image info', 'image_info_s'),
    ('imagenos', 'imagenos_s'),
    ('txtimagename1', 'txtimagename1_s'),
    ('imagecomm', 'imagecomm_s'),
    ('sitedesc', 'sitedesc_s'),
    ('river team', 'river_team_s'),
    ('timepent_s', 'time_spent_s'),
    ('entered by', 'entered_by_s'),
    ('initial date', 'initial_date_s'),
    ('last modified', 'last_modified_s'),
    ('visit comm', 'visit_comm_s'),
    ('Artifacts images', 'Artifacts_THUMBNAILS_ss'),
    ('Map images', 'Map_THUMBNAILS_ss'),
    ('General view images', 'General_view_THUMBNAILS_ss'),
    ('Misc images', 'Misc_THUMBNAILS_ss'),
    ('People images', 'People_THUMBNAILS_ss')

]
FIELD_DEFINITIONS['LIST'] = parmz.LIST

parmz.TABLE = [
    ('id', 'id'),
    ('site name', 'site_name_s'),
    ('short site name', 'site_short_s'),
    ('nrprimrv', 'nrprimrv_s'),
    ('nrsecrv', 'nrsecrv_s'),
    ('vill name', 'vill_name_s'),
    ('village id', 'village_id_s'),
    ('point y', 'point_y_s'),
    ('point x', 'point_x_s'),
    ('oth art', 'oth_art_s'),
]
FIELD_DEFINITIONS['TABLE'] = parmz.TABLE

parmz.GALLERY = [
    ('site name', 'site_name_s'),
]
FIELD_DEFINITIONS['GALLERY'] = parmz.GALLERY

parmz.FULL = [
    ('id', 'id'),
    ('siteid', 'siteid_s'),
    ('site num', 'site_num_s'),
    ('site name', 'site_name_s'),
    ('short site name', 'site_short_s'),
    ('site date', 'site_date_s'),
    ('year recorded', 'year_recorded_s'),
    ('gis code', 'gis_code_s'),
    ('env contxt', 'env_contxt_s'),
    ('access', 'acces_s'),
    ('vill name', 'vill_name_s'),
    ('village id', 'village_id_s'),
    ('nrprimrv', 'nrprimrv_s'),
    ('nrsecrv', 'nrsecrv_s'),
    ('dimena', 'dimena_s'),
    ('dimaorient', 'dimaorient_s'),
    ('dimenb', 'dimenb_s'),
    ('dimborient', 'dimborient_s'),
    ('estdepth', 'estdepth_s'),
    ('exc pri', 'exc_pri_s'),
    ('point y', 'point_y_s'),
    ('point x', 'point_x_s'),
    ('utm x', 'utm_x_s'),
    ('utm y', 'utm_y_s'),
    ('site characteristics', 'site_characteristics_s'),
    ('site comm', 'site_comm_s'),
    ('site conditions', 'site_conditions_s'),
    ('cvmthht', 'cvmthht_s'),
    ('cave fl', 'cave_fl_s'),
    ('cvmthdir', 'cvmthdir_s'),
    ('cavemoist', 'cavemoist_s'),
    ('artdens', 'artdens_s'),
    ('condcomm', 'condcomm_s'),
    ('recent disturbance', 'recent_disturbance_s'),
    ('distcomm', 'distcomm_s'),
    ('pastite functions_s', 'past_site_functions_s'),
    ('pastfcomm', 'pastfcomm_s'),
    ('environment', 'environment_s'),
    ('natveg', 'natveg_s'),
    ('crops', 'crops_s'),
    ('wldedpl', 'wldedpl_s'),
    ('indplant', 'indplant_s'),
    ('fauna', 'fauna_s'),
    ('envcomm', 'envcomm_s'),
    ('artifacts present', 'artifacts_present_s'),
    ('oth art', 'oth_art_s'),
    ('artcomm', 'artcomm_s'),
    ('image info', 'image_info_s'),
    ('imagenos', 'imagenos_s'),
    ('txtimagename1', 'txtimagename1_s'),
    ('imagecomm', 'imagecomm_s'),
    ('sitedesc', 'sitedesc_s'),
    ('river team', 'river_team_s'),
    ('timepent_s', 'time_spent_s'),
    ('entered by', 'entered_by_s'),
    ('initial date', 'initial_date_s'),
    ('last modified', 'last_modified_s'),
    ('visit comm', 'visit_comm_s'),
    ('Artifacts images', 'Artifacts_THUMBNAILS_ss'),
    ('Map images', 'Map_THUMBNAILS_ss'),
    ('General view images', 'General_view_THUMBNAILS_ss'),
    ('Misc images', 'Misc_THUMBNAILS_ss'),
    ('People images', 'People_THUMBNAILS_ss')
]
FIELD_DEFINITIONS['FULL'] = parmz.FULL

FIELD_DEFINITIONS['FACETS'] = parmz.FACETS
parmz.FACET_LABELS = {}
for f in parmz.FACETS:
    parmz.FACET_LABELS[f[1]] = f[0]

parmz.LAYOUTS = 'SEARCH FACETS LIST TABLE GALLERY FULL'.split(' ')
