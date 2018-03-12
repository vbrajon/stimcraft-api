# Stimcraft API
> Stimulate your Starcraft II performance

## Usage
```bash
git clone https://github.com/vbrajon/stimcraft-api.git && cd stimcraft-api
brew install python2
pip2 install -r requirements.txt

brew install parallel jq golang
go get github.com/ericchiang/pup
export PATH=$PATH:~/go/bin
./scrap/scrap-ggtracker.sh
./scrap/scrap-sc2replaystats.sh
./scrap/scrap-spawningtool.sh

# 1201 - 140M - replay/ggtracker
# 2488 - 303M - replay/sc2replaystats
# 2290 - 420M - replay/spawningtool

python2 cli.py replay/ggtracker/7229669.SC2Replay
python2 cli.py -s replay/ggtracker/7229669.SC2Replay

python2 api.py
curl http://127.0.0.1:5000/gg-7229669
curl http://127.0.0.1:5000/gg-7229669?simple=1
```

## Schema
```json
{
  "date": "string",
  "duration": "number",
  "game_format": "string",
  "game_matchup": "string",
  "game_type": "string",
  "map": "string",
  "players": [{
    "_playerId": "number",
    "_slotId": "number",
    "_teamId": "number",
    "_userId": "number",
    "build": [
      ???
    ],
    "clan": "string",
    "color": "string",
    "name": "string",
    "race": "string",
    "race_pref": "string",
    "winner": "boolean"
  }],
  "realm": "number",
  "region": "number",
  "release": "string"
}
```
