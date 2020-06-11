import requests
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from NBA_TEAMS import *
from NBA_TOOLS import *


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


def get_team_stats(team_name):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('log-level=3')
    driver = webdriver.Chrome(chrome_options=options)
    URL = f"https://www.basketball-reference.com/leagues/NBA_2020.html"
    driver.get(URL)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    #
    team_stats_div = soup.find(id="all_team-stats-per_game")
    team_stats_table = team_stats_div.find(id="team-stats-per_game")
    #
    opp_stats_div = soup.find(id="all_opponent-stats-per_game")
    opp_stats_table = opp_stats_div.find(id="opponent-stats-per_game")
    #
    misc_stats_div = soup.find(id="all_misc_stats")
    misc_stats_table = misc_stats_div.find(id="misc_stats")
    th_remove = soup.find(class_="over_header").extract()

    df_list = pd.read_html(str(team_stats_table))
    team_stats_df = df_list[0]

    df_list = pd.read_html(str(opp_stats_table))
    opp_stats_df = df_list[0]

    df_list = pd.read_html(str(misc_stats_table))
    misc_stats_df = df_list[0]

    team_stats_tuple = tuple(
        (team_stats_df.loc[team_stats_df['Team'].str.contains(team_name)]).itertuples(index=False, name=None))
    opp_stats_tuple = tuple(
        (opp_stats_df.loc[opp_stats_df['Team'].str.contains(team_name)]).itertuples(index=False, name=None))
    misc_stats_tuple = tuple(
        (misc_stats_df.loc[misc_stats_df['Team'].str.contains(team_name, na=False)]).itertuples(index=False, name=None))

    return team_stats_tuple, opp_stats_tuple, misc_stats_tuple
