from flask import Flask, request, jsonify
from flask_cache import Cache
from cors import crossdomain
from sc2_extract import sc2_extract
from sc2_transform import sc2_transform

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/<replay_id>')
@crossdomain(origin='*')
def raw(replay_id):
    if (replay_id[:2] == 'gg'): provider = 'ggtracker'
    if (replay_id[:2] == 'ss'): provider = 'sc2replaystats'
    if (replay_id[:2] == 'st'): provider = 'spawningtool'
    if (replay_id[:2] == 'sc'): provider = 'stimcraft'
    replay_file = 'replay/{}/{}.SC2Replay'.format(provider, replay_id[3:])

    if request.args.get('simple'):
        raw = sc2_extract(replay_file)
        data = sc2_transform(raw)
        res = jsonify(data)
    else:
        flag = request.args.get('flag', ','.join(['header', 'details', 'initdata', 'gameevents', 'messageevents', 'trackerevents', 'attributeevents'])).split(',')
        raw = sc2_extract(replay_file, flag=flag)
        res = jsonify(raw)

    res.status_code = 200
    return res

if __name__ == '__main__':
    app.run()
