from flask import Flask
from flask import render_template, jsonify
import urllib.request, json
import urllib.error
app = Flask(__name__)


@app.route('/schedule')
def schedule():
    with urllib.request.urlopen(
        "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
    ) as url:
        data = json.load(url)
        scoreboard = data['scoreboard']
        games = scoreboard['games']
        games_dict = []
        for game in games:
            temp_dict = {
                'away': game['awayTeam']['teamTricode'],
                'a_score': game['awayTeam']['score'],
                'home': game['homeTeam']['teamTricode'],
                'h_score':game['homeTeam']['score'],
                'time': game['gameEt'],
                'a_to': game['awayTeam']['timeoutsRemaining'],
                'h_to': game['homeTeam']['timeoutsRemaining'],
                'game_id': game['gameId'],
                'a_bonus': game['awayTeam']['inBonus'],
                'h_bonus': game['homeTeam']['inBonus'],
                'clock': game['gameClock']}
            games_dict.append(temp_dict)
        return(games_dict)

@app.route('/data_json')
def data_json():
    sched = schedule()
    table_dict = []
    index = 0
    for s in sched:
        try:
            full_url = "https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_" + s['game_id'] + ".json"
            with urllib.request.urlopen(full_url) as url:
                data = json.load(url)
            pbp = data['game']['actions'].pop()
            index += 1
            temp_dict = {
                'id': index,
                'away': s['away'],
                'a_score': s['a_score'],
                'home': s['home'],
                'h_score': s['h_score'],
                'time': s['time'],
                'a_to': s['a_to'],
                'h_to': s['h_to'],
                'a_bonus': s['a_bonus'],
                'h_bonus': s['h_bonus'],
                'clock': s['clock'],
                'state': pbp['actionType'],
                'desc': pbp['subType'],
                'detail': pbp['description']
            }
            table_dict.append(temp_dict)
        except urllib.error.HTTPError as e:
            temp = "error"
    return(jsonify(table_dict))




@app.route('/')
def index():
    dummy_data = data_json()
    return render_template(
        'index.html',
        matches=dummy_data.json,
    )


if __name__ == '__main__':
    app.run()
