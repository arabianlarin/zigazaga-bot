import requests
import pandas as pd
from datetime import datetime
import os
from time import sleep
import duckdb

class teamsData:
    def __init__(self, teams, team_lookup):
        self.teams = teams
        self.team_lookup = team_lookup

class bootstrapData:
    def __init__(self, players, averages):
        self.players = players
        self.averages = averages

def get_positions():
    return pd.DataFrame({
            'element_type': [1, 2, 3, 4],
            'position': ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']
            })

#@st.cache_data(ttl=3600)
def get_bootstrap():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = requests.get(url)
    data = response.json()
    events = data['events']
    players = pd.DataFrame(data['elements'])
    players = players[['first_name',
                        'second_name',
                        'form',
                        'now_cost',
                        'photo',
                        'selected_by_percent',
                        'id',
                        'team',
                        'total_points',
                        'web_name',
                        'influence',
                        'creativity',
                        'threat',
                        'ict_index',
                        'defensive_contribution',
                       'minutes',
                       'element_type',
                       'expected_goals_conceded_per_90'
                      ]]
    players = duckdb.query('''
    select concat(first_name, ' ', second_name) player_name, * from players
    '''
    ).to_df()
    pos = get_positions()
    players = duckdb.query('''select p.*, position from players p left join pos using(element_type)''').to_df()
    averages = pd.DataFrame([{
        'gameweek': e['id'],
        'name': 'Average',
        'average_points': e['average_entry_score']
    } for e in events if e['finished']])
    return bootstrapData(players, averages)
    
# def get_player_history():
#     url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
#     response = requests.get(url)
#     data = response.json()
#     players = pd.DataFrame(data['elements'])
#     return players[['id', 'web_name', 'first_name', 'second_name', 'team', 'element_type', 'now_cost', 'selected_by_percent', 'total_points']]

#@st.cache_data(ttl=3600)
def get_teams():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = requests.get(url)
    data = response.json()
    teams = pd.DataFrame(data['teams'])
    teams = teams[['id', 'name', 'short_name']]
    team_lookup = teams.set_index('id')['name'].to_dict()
    return teamsData(teams, team_lookup)
