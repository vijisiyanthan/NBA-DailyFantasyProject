import requests
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup


def get_team_stats(team_name):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
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


if __name__ == '__main__':
    get_team_stats("TORONTO_RAPTORS")
