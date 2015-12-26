from flask import Flask, jsonify
import csv
import json
from utils import get_ncaa_data

import sys

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

app = Flask(__name__)

@app.route('/api/v1.0/<string:sport_code>/<string:div>/teams/', defaults={'academic_year': 'latest'}, methods=['GET'])
@app.route('/api/v1.0/<string:sport_code>/<string:div>/<string:academic_year>/teams/', methods=['GET'])
def get_teams(sport_code, div, academic_year):
    """
    Returns latest data of all teams. Output is a JSON dictionary with 'response' 
    as the key and a list of objects for each team as the value.
    
    :param sport_code:
        NCAA code for desired sport. Ex: 'MBB' is Men's Basketball
    :param div:
        NCAA division. Ex: '1' for Division 1.
    :param academic_year:
        (Optional) Four digit academic year. Ex: '2015' for 2014-2015. Defaults to 'latest'.
    """    
    reader = csv.DictReader(StringIO(get_ncaa_data(sport_code=sport_code, div=div, stat_seq='team', academic_year=academic_year)))
    return jsonify({'response': list(reader)})

@app.route('/api/v1.0/<string:sport_code>/<string:div>/teams/<string:team_name>', defaults={'academic_year': 'latest'}, methods=['GET'])    
@app.route('/api/v1.0/<string:sport_code>/<string:div>/<string:academic_year>/teams/<string:team_name>', methods=['GET'])
def get_team(sport_code, div, academic_year, team_name):
    """
    Returns latest data of specified team. Output is a JSON dictionary with 'response' 
    as the key and a list of objects for each team as the value.
    
    :param sport_code:
        NCAA code for desired sport. Ex: 'MBB' is Men's Basketball
    :param div:
        NCAA division. Ex: '1' for Division 1.
    :param academic_year:
        (Optional) Four digit academic year. Ex: '2015' for 2014-2015. Defaults to 'latest'.
    :param team_name:
        NCAA school name with spaces removed.
    """  
    reader = csv.DictReader(StringIO(utils.get_ncaa_data(sport_code=sport_code, div=div, stat_seq='team', academic_year=academic_year)))
    
    team_obj = {}
    for team in reader:
        if team['Name'].replace(' ', '') == team_name:
            team_obj = team
            break
            
    return jsonify({'response': [team_obj]})

@app.route('/api/v1.0/<string:sport_code>/<string:div>/players/', defaults={'academic_year': 'latest'}, methods=['GET'])
@app.route('/api/v1.0/<string:sport_code>/<string:div>/<string:academic_year>/players/', methods=['GET'])
def get_players(sport_code, div, academic_year):    
    """
    Returns latest data of all players. Output is a JSON dictionary with 'response' 
    as the key and a list of objects for each player as the value. Warning: many 
    players have blanks in columns.
    
    :param sport_code:
        NCAA code for desired sport. Ex: 'MBB' is Men's Basketball
    :param div:
        NCAA division. Ex: '1' for Division 1.
    :param academic_year:
        (Optional) Four digit academic year. Ex: '2015' for 2014-2015. Defaults to 'latest'.
    """ 
    reader = csv.DictReader(StringIO(utils.get_ncaa_data(sport_code=sport_code, div=div, stat_seq='player', academic_year=academic_year)))
    return jsonify({'response': list(reader)})

@app.route('/api/v1.0/<string:sport_code>/<string:div>/players/<string:player_name>', defaults={'academic_year': 'latest'}, methods=['GET'])
@app.route('/api/v1.0/<string:sport_code>/<string:div>/<string:academic_year>/players/<string:player_name>', methods=['GET'])
def get_player(sport_code, div, academic_year, player_name):
    """
    Returns latest data of specified player. Output is a JSON dictionary with 'response' 
    as the key and a list of objects for each player as the value. Warning: many 
    players have blanks in columns.
    
    :param sport_code:
        NCAA code for desired sport. Ex: 'MBB' is Men's Basketball
    :param div:
        NCAA division. Ex: '1' for Division 1.
    :param academic_year:
        (Optional) Four digit academic year. Ex: '2015' for 2014-2015. Defaults to 'latest'.
    :param player_name:
        Player name with spaces removed.
    """ 
    reader = csv.DictReader(StringIO(utils.get_ncaa_data(sport_code=sport_code, div=div, stat_seq='player', academic_year=academic_year)))
    
    player_obj = {}
    for player in reader:
        if player['Name'].replace(' ', '') == player_name:
            player_obj = player
            break
            
    return jsonify({'response': [player_obj]})

if __name__ == "__main__":
    app.run(debug=True)
