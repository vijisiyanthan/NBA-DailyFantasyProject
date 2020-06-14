import pandas as pd
import sqlite3


def get_team_stats():
    # Pulling stats from table in fantasy.db
    conn = sqlite3.connect("fantasy.db")
    df_team_stats = pd.read_sql_query("SELECT * FROM team_stats;", conn)
    df_misc_stats = pd.read_sql_query("SELECT * FROM misc_stats;", conn)
    df_opp_stats = pd.read_sql_query("SELECT * FROM opp_stats;", conn)
    # Remove unneeded index and Rk  columns in all dataframe tables
    columns = ['index', 'Rk']
    df_team_stats = df_team_stats.drop(columns=columns)
    df_misc_stats = df_misc_stats.drop(columns=columns)
    df_opp_stats = df_opp_stats.drop(columns=columns)
    # Modify opp_stats and modify column names to reflect opp
    df_opp_stats = df_opp_stats.drop(columns=['G', 'MP'])
    column_name = df_opp_stats.columns
    changed_column = list()
    for name in column_name:
        if name != 'Team':
            name = f"Opp{str(name)}"
            changed_column.append(name)
        else:
            changed_column.append(name)
    # Modify df_misc_stats and drop unneeded column names
    df_misc_stats = df_misc_stats.drop(columns=['Arena', 'Attend.', 'Attend./G'])
    df_opp_stats.columns = changed_column
    # Merge Three Dataframe tables
    df_team_stats = pd.merge(df_team_stats, df_opp_stats, on='Team')
    df_team_stats = pd.merge(df_team_stats, df_misc_stats, on='Team')
    return df_team_stats


def get_player_stats():
    # Pulling stats from table in fantasy.db
    conn = sqlite3.connect("fantasy.db")
    df_players_total_stats = pd.read_sql_query("SELECT * FROM players_total_stats;", conn)
    df_players_adv_stats = pd.read_sql_query("SELECT * FROM players_adv_stats;", conn)
    df_players_boxscores = pd.read_sql_query("SELECT * FROM player_boxscores;", conn)

    df_players_boxscores = df_players_boxscores.drop(columns=['level_0', 'index'])
    df_players_total_stats = df_players_total_stats.drop(columns=['index'])
    df_players_adv_stats = df_players_adv_stats.drop(
        columns=['index', 'team', 'name', 'positions', 'age', 'games_played', 'minutes_played'])

    df_players_total_stats = pd.merge(df_players_total_stats, df_players_adv_stats, on='slug')

    return df_players_total_stats, df_players_boxscores


class FantasyDatabase:
    team_stats = None
    player_stats = None
    boxscores = None

    def __init__(self):
        self.team_stats = get_team_stats()
        self.player_stats, self.boxscores = get_player_stats()
