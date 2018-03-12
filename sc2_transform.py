from toolz import groupby
from datetime import datetime

def windows_to_unix(windows_time):
    # This windows timestamp measures the number of 100 nanosecond periods since
    # January 1st, 1601. First we subtract the number of nanosecond periods from
    # 1601-1970, then we divide by 10^7 to bring it back to seconds.
    return int((windows_time - 116444735995904000) / 10 ** 7)


def find_player(player):
    slot = next(s for s in i['m_syncLobbyState']['m_lobbyState']['m_slots']
        if s["m_workingSetSlotId"] == player["m_workingSetSlotId"])
    data = i['m_syncLobbyState']['m_userInitialData'][slot['m_userId']]
    setup = next(e for e in t
        if e['_event'] == 'NNet.Replay.Tracker.SPlayerSetupEvent'
        and e['m_userId'] == slot['m_userId'])
    color = '#%02x%02x%02x' % tuple([player['m_color'][key] for key in ('m_r', 'm_g', 'm_b')])

    units = ['scv', 'marine', 'marauder', 'reaper', 'ghost', 'hellion', 'siege-tank', 'thor', 'viking', 'medivac', 'raven', 'banshee', 'battlecruiser', 'hellbat', 'widow-mine', 'liberator', 'cyclone', 'probe', 'zealot', 'stalker', 'sentry', 'observer', 'immortal', 'warp-prism', 'colossus', 'phoenix', 'void-ray', 'high-templar', 'dark-templar', 'archon', 'carrier', 'mothership', 'mothership-core', 'oracle', 'tempest', 'adept', 'disruptor', 'drone', 'overlord', 'zergling', 'queen', 'hydralisk', 'baneling', 'overseer', 'roach', 'infestor', 'mutalisk', 'corruptor', 'nydus-worm', 'ultralisk', 'brood-lord', 'swarm-host', 'viper', 'ravager', 'lurker']
    buildings = ['command-center', 'supply-depot', 'refinery', 'barracks', 'orbital-command', 'planetary-fortress', 'engineering-bay', 'bunker', 'missile-turret', 'sensor-tower', 'factory', 'ghost-academy', 'armory', 'starport', 'fusion-core', 'tech-lab', 'reactor', 'nexus', 'pylon', 'assimilator', 'gateway', 'forge', 'photon-cannon', 'warpgate', 'cybernetics-core', 'twilight-council', 'robotics-facility', 'stargate', 'templar-archives', 'dark-shrine', 'robotics-bay', 'fleet-beacon',  'evolution-chamber', 'hatchery', 'extractor', 'spawning-pool', 'spine-crawler', 'spire', 'roach-warren', 'infestation-pit', 'spore-crawler', 'hydralisk-den', 'baneling-nest', 'lair', 'nydus-network', 'hive', 'ultralisk-cavern', 'greater-spire']

    build = [[
        e['_gameloop'] / 24,
        e['m_unitTypeName']
    ] for e in t
        if 'm_unitTypeName' in e
        and 'm_controlPlayerId' in e
        and e['_gameloop'] is not 0
        and e['m_unitTypeName'].lower() in units + buildings
        and e['m_controlPlayerId'] is setup['m_playerId']
    ]

    return {
        '_playerId': setup['m_playerId'],
        '_slotId': setup['m_slotId'],
        '_teamId': slot['m_teamId'],
        '_userId': slot['m_userId'],
        'build': build,
        'clan': data['m_clanTag'],
        'color': color,
        'name': data['m_name'],
        'race_pref': ('T', 'Z', 'P')[slot['m_racePref']['m_race']],
        'race': player['m_race'][0],
        'winner': player['m_result'] == 1,
    }


def sc2_transform(raw):
    global h,d,i,g,m,t
    h = raw['header']
    d = raw['details']
    i = raw['initdata']
    g = raw['gameevents']
    m = raw['messageevents']
    t = raw['trackerevents']

    duration = g[-1]['_gameloop'] / 24
    start = datetime.utcfromtimestamp(windows_to_unix(d['m_timeUTC']) - duration * 1000).isoformat()

    teams = groupby(lambda x: x['m_teamId'], d['m_playerList']).values()
    game_options = i['m_syncLobbyState']['m_gameDescription']['m_gameOptions']
    game_format = 'v'.join([str(len(team)) for team in teams])
    game_type = ('Custom', 'Unranked', 'Ranked')[game_options['m_amm'] + game_options['m_competitive']]
    game_matchup = 'v'.join(['-'.join(p['m_race'][0] for p in team) for team in teams])

    players = [find_player(player) for team in teams for player in team]

    return {
        'date': start,
        'duration': duration,
        'game_format': game_format,
        'game_type': game_type,
        'game_matchup': game_matchup,
        'map': d['m_title'],
        'players': players,
        'realm': d['m_playerList'][0]['m_toon']['m_realm'],
        'region': d['m_playerList'][0]['m_toon']['m_region'],
        'release': '.'.join([str(h['m_version'][key]) for key in ['m_major', 'm_minor', 'm_revision', 'm_build']]),
    }
