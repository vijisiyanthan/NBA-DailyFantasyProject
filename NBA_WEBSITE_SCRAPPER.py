from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from NBA_TOOLS import *
import pandas as pd



def get_roster_player_list(team):

    client.players_advanced_season_totals(season_end_year=2020, output_type=OutputType.CSV,
                                          output_file_path="./csv/advanced_players.csv")

    client.players_season_totals(season_end_year=2020, output_type=OutputType.CSV,
                                 output_file_path="./csv/season_totals.csv")

    df_advanced_stats = pd.read_csv("./csv/advanced_players.csv")
    df_total_season_stats = pd.read_csv("./csv/season_totals.csv")

    players_advanced_roster_stats = df_advanced_stats.loc[df_advanced_stats['team'].str.contains(team.name[1].upper())]
    players_total_roster_stats = df_total_season_stats.loc[df_advanced_stats['team'].str.contains(team.name[1].upper())]

    return players_advanced_roster_stats, players_total_roster_stats


def set_season_schedule(player_ids):
    df = pd.DataFrame()
    for id in player_ids:
        client.regular_season_player_box_scores(player_identifier=id, season_end_year=2020,
                                                output_type=OutputType.CSV,
                                                output_file_path=f"./csv/boxscores/{id}_box_scores.csv")
    for id in player_ids:
        df_season_schedule = pd.read_csv(f"./csv/boxscores/{id}_box_scores.csv")
        df_season_schedule['slug'] = id
        df = pd.concat([df, df_season_schedule])

    df['date'] = pd.to_datetime(df['date'])
    dates = df['date']
    dates = dates.reset_index()
    dates = dates.date.unique()
    dates.sort()
    last_game_date = pd.Timestamp((max(dates))).to_datetime64()
    game_fifteen_date = pd.Timestamp(dates[-15]).to_datetime64()
    boxscores = (df.loc[(df['date'] >= game_fifteen_date) & (df['date'] <= last_game_date)])
    boxscores = boxscores.reset_index()
    return boxscores


def get_team_stats(team_name, team_stats_df, opp_stats_df, misc_stats_df):
    team_stats_row = (team_stats_df.loc[team_stats_df['Team'].str.contains(team_name)])
    opp_stats_row = (opp_stats_df.loc[opp_stats_df['Team'].str.contains(team_name)])
    misc_stats_row = (misc_stats_df.loc[misc_stats_df['Team'].str.contains(team_name, na=False)])

    return team_stats_row, opp_stats_row, misc_stats_row

