from flask import Flask, jsonify
from boknows import utils
import csv
import json

import sys

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

app = Flask(__name__)

@app.route('/api/v1.0/<string:sport_code>/<string:div>/teams', methods=['GET'])
def get_teams(sport_code, div):
    """
    Returns latest data of all teams. Output is a JSON dictionary with 'response' 
    as the key and a list of objects for each team as the value.
    
    :param sport_code:
        NCAA code for desired sport. Ex: 'MBB' is Men's Basketball
    :param div:
        NCAA division. Ex: '1' for Division 1.
    """    
    reader = csv.DictReader(StringIO(utils.get_ncaa_data(sport_code, div, 'team')))
    return jsonify({'response': list(reader)})
    
@app.route('/api/v1.0/<string:sport_code>/<string:div>/teams/<string:team_name>', methods=['GET'])
def get_team(sport_code, div, team_name):
    """
    Returns latest data of specified team. Output is a JSON dictionary with 'response' 
    as the key and a list of objects for each team as the value.
    
    :param sport_code:
        NCAA code for desired sport. Ex: 'MBB' is Men's Basketball
    :param div:
        NCAA division. Ex: '1' for Division 1.
    :param team_name:
        NCAA school name with spaces removed.
    """  
    reader = csv.DictReader(StringIO(utils.get_ncaa_data(sport_code, div, 'team')))
    
    team_obj = {}
    for team in reader:
        if team['Name'].replace(' ', '') == team_name:
            team_obj = team
            break
            
    return jsonify({'response': [team_obj]})

@app.route('/api/v1.0/<string:sport_code>/<string:div>/players', methods=['GET'])
def get_players(sport_code, div):    
    """
    Returns latest data of all players. Output is a JSON dictionary with 'response' 
    as the key and a list of objects for each player as the value. Warning: many 
    players have blanks in columns.
    
    :param sport_code:
        NCAA code for desired sport. Ex: 'MBB' is Men's Basketball
    :param div:
        NCAA division. Ex: '1' for Division 1.
    """ 
    reader = csv.DictReader(StringIO(utils.get_ncaa_data(sport_code, div, 'player')))
    return jsonify({'response': list(reader)})
    
@app.route('/api/v1.0/<string:sport_code>/<string:div>/players/<string:player_name>', methods=['GET'])
def get_player(sport_code, div, player_name):
    """
    Returns latest data of specified player. Output is a JSON dictionary with 'response' 
    as the key and a list of objects for each player as the value. Warning: many 
    players have blanks in columns.
    
    :param sport_code:
        NCAA code for desired sport. Ex: 'MBB' is Men's Basketball
    :param div:
        NCAA division. Ex: '1' for Division 1.
    :param player_name:
        Player name with spaces removed.
    """ 
    reader = csv.DictReader(StringIO(utils.get_ncaa_data(sport_code, div, 'player')))
    
    player_obj = {}
    for player in reader:
        if player['Name'].replace(' ', '') == player_name:
            player_obj = player
            break
            
    return jsonify({'response': [player_obj]})

if __name__ == "__main__":
    app.run(debug=True)
