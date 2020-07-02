import LoadBBallData
from FANTASY_DATABASE import FantasyDatabase
import projections
import pandas as pd
from sys import argv


def remove_player():
    players_playing = bball_db.boxscores['slug'].unique()
    bball_db.player_stats = bball_db.player_stats[bball_db.player_stats['slug'].isin(players_playing)]
    # print(players_playing)


def set_players_not_playing():
    name = ""
    print("Input inactive players: (type done once completed)")
    while name != 'done':
        name = input("Enter player name: ").lower()
        slug = bball_db.player_stats[bball_db.player_stats['name'].str.lower() == name]
        if slug.empty:
            print("Not Found!")
        else:
            slug = slug['slug'].values[0]
            bball_db.boxscores = bball_db.boxscores[bball_db.boxscores['slug'] != slug]
            bball_db.player_stats = bball_db.player_stats[bball_db.player_stats['name'].str.lower() != name]
            print(f"Removed, {name}!")
    bball_db.boxscores = bball_db.boxscores.loc[(bball_db.boxscores['minutes_played'] >= 15)]
    remove_player()


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.options.mode.chained_assignment = None  # default='warn'
    # teams_playing = LoadBBallData.get_games_today()
    bball_db = FantasyDatabase()
    set_players_not_playing()
    player_stats_combined = projections.combine_stats(bball_db.team_stats, bball_db.player_stats, bball_db.boxscores)
    # implement minutes, currently using starting lineups to set minutes
    df_projections_starters = projections.set_starter_minutes(player_stats_combined, bball_db.lineups)
    df_final_projections, good_matchups_lst, alright_matchups_lst, meh_matchups_lst = projections.set_boosters(
        df_projections_starters, bball_db.team_stats,
        bball_db.matchups)
    projections.optimize_lineup(df_final_projections, good_matchups_lst, alright_matchups_lst, meh_matchups_lst)
