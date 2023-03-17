import os
import sys
import obspython as obs

debug = False
script_settings = ''
source_name = ''
search_string = ''


def script_description():
    return 'Look for a string in the current log file and notify the user in a text source if found.'


def script_properties():
    props = obs.obs_properties_create()

    # add text box at the settings page
    obs.obs_properties_add_text(props, 'searchstring', 'Search in log:', obs.OBS_TEXT_DEFAULT)

    # show a list of text sources to choose where to display the error
    props_list = obs.obs_properties_add_list(props, 'source', 'Text Source', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id == 'text_gdiplus' or source_id == 'text_ft2_source':
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(props_list, name, name)
    obs.source_list_release(sources)
    return props


def script_load(settings):
    """
    Called when loading the script
    """

    # make settings available everywhere
    global script_settings
    script_settings = settings

    obs.obs_frontend_add_event_callback(event_handler)


def script_update(settings):
    # user set some config
    global source_name, search_string
    source_name = obs.obs_data_get_string(settings, 'source')
    search_string = obs.obs_data_get_string(settings, 'searchstring')


def refresh_pressed(props, prop):
    """
    Called when the 'refresh' button defined below is pressed
    """
    update_text('Reloaded!')


def script_unload():
    """
    Called when unloading the script
    """
    update_text('Unloaded!')
    obs.obs_data_release(script_settings)


def event_handler(event):
    if event in (obs.OBS_FRONTEND_EVENT_FINISHED_LOADING, obs.OBS_FRONTEND_EVENT_SCENE_COLLECTION_CHANGED):
        # empty the text source before checking
        text = ''
        update_text(text)

        check_log(script_settings)


def check_log(settings):
    log_dir = os.getenv('appdata') + '/obs-studio/logs/'
    log_list = sorted(os.listdir(log_dir))
    log_file = log_list[-1]
    if debug:
        # create this file next to the logs with the string you are looking for
        log_file = '1debug.txt'
    l = open(log_dir + log_file, 'r')
    log = l.read()
    l.close()

    if search_string in log:
        text = 'Log has error'
        update_text(text)


def update_text(text):
    source = obs.obs_get_source_by_name(source_name)
    if source:
        obs.obs_data_set_string(script_settings, 'text', text)
        obs.obs_source_update(source, script_settings)
        obs.obs_source_release(source)
