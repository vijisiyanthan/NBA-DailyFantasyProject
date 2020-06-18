import urllib.request
import json
import pandas as pd
import sqlite3
import FantasySites


def get_team_stats():
    # Pulling stats from table in fantasy.db
    conn = sqlite3.connect("fantasy.db")
    df_misc_stats = pd.read_sql_query("SELECT * FROM misc_stats;", conn)
    # Remove unneeded index and Rk  columns in all dataframe tables
    columns = ['index', 'Rk']
    df_misc_stats = df_misc_stats.drop(columns=columns)
    final_columns = ['Team','MOV', 'ORtg', 'DRtg', 'Pace', 'FTr', '3PAr', 'eFG%', 'TOV%', 'ORB%', 'FT/FGA', 'eFG%.1', 'TOV%.1',
                     'DRB%', 'FT/FGA.1']
    df_misc_stats = df_misc_stats[final_columns]
    df_misc_stats = df_misc_stats.rename(
        columns={'eFG%.1': 'oppEFG%', 'TOV%.1': 'oppTOV%', 'FT/FGA.1': 'oppFT/FGA', 'eFG%': 'EFG%'})

    final_columns = ['MOV', 'ORtg', 'DRtg', 'Pace', 'FTr', '3PAr', 'EFG%', 'TOV%', 'ORB%', 'FT/FGA', 'oppEFG%', 'oppTOV%',
                     'DRB%', 'oppFT/FGA']

    df_misc_stats[final_columns] = df_misc_stats[final_columns].astype(float)
    return df_misc_stats


def get_player_stats():
    # Pulling stats from table in fantasy.db
    conn = sqlite3.connect("fantasy.db")
    df_players_total_stats = pd.read_sql_query("SELECT * FROM players_total_stats;", conn)
    df_players_adv_stats = pd.read_sql_query("SELECT * FROM players_adv_stats;", conn)
    df_players_boxscores = pd.read_sql_query("SELECT * FROM player_boxscores;", conn)

    df_players_total_stats = df_players_total_stats.drop(columns=['index'])

    # Handling Team Stats Data
    df_players_total_stats['Fantasy Points Scored'] = df_players_total_stats.apply(
        lambda row: (((row.made_field_goals - row.made_three_point_field_goals) * 2) + (
                row.made_three_point_field_goals * 3) + row.made_free_throws + (
                             row.offensive_rebounds + row.defensive_rebounds) * 1.2 + (row.assists * 1.5) + (
                             row.steals + row.blocks) * 3) - row.turnovers, axis=1)
    df_players_total_stats['FPS/G'] = df_players_total_stats['Fantasy Points Scored'] / df_players_total_stats[
        'games_played']
    df_players_total_stats['MIN/G'] = df_players_total_stats['minutes_played'] / df_players_total_stats['games_played']
    df_players_total_stats['FPS/M'] = df_players_total_stats['Fantasy Points Scored'] / df_players_total_stats[
        'minutes_played']

    df_players_total_stats = df_players_total_stats[
        ['slug', 'name', 'team', 'positions', 'games_played', 'FPS/G', 'MIN/G', 'FPS/M']]

    # Handling advanced player stats
    df_players_adv_stats = df_players_adv_stats.drop(
        columns=['index', 'team', 'name', 'positions', 'age', 'games_played', 'minutes_played',
                 'offensive_rebound_percentage', 'defensive_rebound_percentage'])

    df_players_total_stats = pd.merge(df_players_total_stats, df_players_adv_stats, on='slug')

    # Handling Boxscore Data
    df_players_boxscores['Fantasy Points Scored'] = df_players_boxscores.apply(
        lambda row: (((row.made_field_goals - row.made_three_point_field_goals) * 2) + (
                row.made_three_point_field_goals * 3) + row.made_free_throws + (
                             row.offensive_rebounds + row.defensive_rebounds) * 1.2 + (row.assists * 1.5) + (
                             row.steals + row.blocks) * 3) - row.turnovers, axis=1)
    df_players_boxscores['A/TO'] = df_players_boxscores.apply(
        lambda row: 0 if row.turnovers == 0 else row.assists / row.turnovers, axis=1)

    df_players_boxscores['ThreePointRate'] = df_players_boxscores.apply(
        lambda
            row: 0 if row.attempted_field_goals == 0 else row.attempted_three_point_field_goals / row.attempted_field_goals,
        axis=1)

    df_players_boxscores = df_players_boxscores[
        ['date', 'slug', 'team', 'location', 'opponent', 'outcome', 'Fantasy Points Scored', 'A/TO', 'ThreePointRate']]

    #####

    return df_players_total_stats, df_players_boxscores


def get_output_string(team_name):
    output_str = str()
    for e in range(len(team_name) - 1):
        output_str = output_str + team_name[e] + "-"
    output_str = output_str + team_name[len(team_name) - 1]
    return output_str.lower()


def get_team_lineups(teams_names):
    lineups = dict()
    for team in teams_names:
        team_name = str(team).split(' ')
        output_str = get_output_string(team_name)
        urlreq = f'https://api.lineups.com/nba/fetch/lineups/current/{output_str}'
        response = urllib.request.urlopen(urlreq)
        jresponse = json.load(response)

        starters = jresponse['starters']
        past_lineups = jresponse['past_lineups']
        freq_lineups = jresponse['frequent_lineups']

        lst_past_lineups = dict()
        lst_freq_lineups = dict()
        lst_starters = list()

        for i in range(5):
            lineup = past_lineups[i]
            result = lineup['result']
            game = str(lineup['game']).split(' vs')
            lst_players = dict()
            for n in range(1, 6):
                name = lineup[str(n)]['name']
                position = lineup[str(n)]['position']
                lst_players.update({name: position})
            lst_past_lineups.update({game[0]: lst_players.items()})

        for i in range(5):
            lineup = freq_lineups[i]['players']
            frequency = freq_lineups[i]['frequency']
            lst_players = dict()
            for n in range(5):
                name = lineup[n]['name']
                position = lineup[n]['position']
                lst_players.update({name: position})
            lst_freq_lineups.update({frequency: lst_players.items()})

        for i in range(5):
            name = starters[i]['name']
            position = starters[i]['position']
            lst_starters.append({name: position})

        team_lineup = team_lineups(lst_starters, lst_past_lineups, lst_freq_lineups)
        lineups.update({team: team_lineup})

    return lineups


class team_lineups():
    def __init__(self, starters, past, freq):
        self.starters = starters
        self.past = past
        self.freq = freq


class FantasyDatabase:
    team_stats = None
    player_stats = None
    boxscores = None
    lineups = None

    def __init__(self):
        self.team_stats = get_team_stats()
        self.player_stats, self.boxscores = get_player_stats()
        self.lineups = get_team_lineups(self.player_stats['team'].unique())
