import mpyq
from s2protocol.versions import protocol15405

def sc2_extract(replay_file, flag=['header', 'details', 'initdata', 'gameevents', 'messageevents', 'trackerevents', 'attributeevents']):
    archive = mpyq.MPQArchive(replay_file)

    # Read the protocol header, this can be read with any protocol
    contents = archive.header['user_data_header']['content']
    headr = protocol15405.decode_replay_header(contents)

    # The header's baseBuild determines which protocol to use
    baseBuild = headr['m_version']['m_baseBuild']
    package = 's2protocol.versions'
    module = 'protocol%s' % (baseBuild)
    protocol = getattr(__import__(package, fromlist=[module]), module)

    data = {}
    if 'header' in flag:
        data['header'] = headr

    # Store protocol details
    if 'details' in flag:
        contents = archive.read_file('replay.details')
        data['details'] = protocol.decode_replay_details(contents)
        del data['details']['m_cacheHandles']

    # Store protocol init data
    if 'initdata' in flag:
        contents = archive.read_file('replay.initData')
        data['initdata'] = protocol.decode_replay_initdata(contents)
        del data['initdata']['m_syncLobbyState']['m_gameDescription']['m_cacheHandles']

    # Store game events and/or game events stats
    if 'gameevents' in flag:
        contents = archive.read_file('replay.game.events')
        data['gameevents'] = [event for event in protocol.decode_replay_game_events(contents)]

    # Store message events
    if 'messageevents' in flag:
        contents = archive.read_file('replay.message.events')
        data['messageevents'] = [event for event in protocol.decode_replay_message_events(contents)]

    # Store tracker events
    if 'trackerevents' in flag:
        if hasattr(protocol, 'decode_replay_tracker_events'):
            contents = archive.read_file('replay.tracker.events')
            data['trackerevents'] = [event for event in protocol.decode_replay_tracker_events(contents)]

    # Store attributes events
    if 'attributeevents' in flag:
        contents = archive.read_file('replay.attributes.events')
        data['attributeevents'] = [event for event in protocol.decode_replay_attributes_events(contents)]

    return data
