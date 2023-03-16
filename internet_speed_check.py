import speedtest
import obspython as obs
from asyncio import run

debug = False
source_name = ''
script_settings = ''


def script_description():
    return '''
    <b>Do a speedtest before a stream to check your internet connection.</b>
    <ul>
        <li>Result is shown in the choosen text source</li>
        <li>This text source will be hidden if recording starts</li>
        <li>You need to install the python module speedtest on your set python installation</li>
    </ul>
    '''


def script_properties():
    props = obs.obs_properties_create()

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
    update_text('Started!')
    if obs.obs_initialized():
        speed = run(speed_check())
        update_text(speed)


def script_unload():
    """
    Called when unloading the script
    """
    update_text('Unloaded!')
    obs.obs_data_release(script_settings)
    obs.obs_source_release(source)


def script_update(settings):
    # user set some config
    global source_name
    source_name = obs.obs_data_get_string(settings, 'source')


def refresh_pressed(props, prop):
    """
    Called when the 'refresh' button defined below is pressed
    """
    update_text('Reloaded!')


def event_handler(event):
    if event in (obs.OBS_FRONTEND_EVENT_FINISHED_LOADING, obs.OBS_FRONTEND_EVENT_SCENE_COLLECTION_CHANGED):
        speed = run(speed_check())
        update_text(speed)
    elif event == obs.OBS_FRONTEND_EVENT_RECORDING_STARTING:
        obs.obs_source_set_enabled(source, False)
    elif event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        obs.obs_source_set_enabled(source, True)
    elif event == obs.OBS_FRONTEND_EVENT_SCRIPTING_SHUTDOWN:
        pass


async def speed_check():
    update_text('Speed testing...')
    threads = 10
    if debug:
        # rate limits :)
        from random import randrange
        return (randrange(10000000, 100000000) / 1048576, randrange(0, 100))
    s = speedtest.Speedtest()
    s.upload(threads=threads)
    return (s.results.upload / 1048576, s.results.ping)


def update_text(speed):
    # Check if it's text we got or the result of the speedtest
    if isinstance(speed, tuple):
        text = f'Upload: {int(speed[0])}\nPing: {speed[1]}'
    else:
        text = speed
    source = obs.obs_get_source_by_name(source_name)
    if source:
        obs.obs_data_set_string(script_settings, 'text', text)
        obs.obs_source_update(source, script_settings)
