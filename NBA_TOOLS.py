import NBA_TEAMS
import NBA_WEBSITE_SCRAPPER
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup


def get_league_teams_stats():
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
    misc_stats_div = soup.find(id="all_misc_stats")
    misc_stats_table = misc_stats_div.find(id="misc_stats")
    th_remove = soup.find(class_="over_header").extract()

    df_list = pd.read_html(str(misc_stats_table))
    misc_stats_df = df_list[0]
    misc_stats_df = misc_stats_df.dropna()
    misc_stats_df = misc_stats_df.loc[misc_stats_df['Team'] != 'Team']

    return misc_stats_df


class League:
    teams_misc = None

    def __init__(self):
        self.teams_misc = get_league_teams_stats()


class Team:
    name = None
    abr = None
    misc_stats = None
    adv_player_stats = None
    total_player_stats = None
    boxscores = None

    def __init__(self, name, league):
        self.name = name
        self.misc_stats = NBA_WEBSITE_SCRAPPER.get_team_stats(
            name[1], misc_stats_df=league.teams_misc)
        self.adv_player_stats, self.total_player_stats = NBA_WEBSITE_SCRAPPER.get_roster_player_list(self)
        self.boxscores = NBA_WEBSITE_SCRAPPER.set_season_schedule(self.adv_player_stats['slug'])
