import NBA_TEAMS
import NBA_WEBSITE_SCRAPPER
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup


class League:
    teams_season = None
    teams_opp = None
    teams_misc = None
    teams_schedule = None

    def __init__(self):
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

        self.teams_misc = misc_stats_df
        self.teams_opp = opp_stats_df
        self.teams_season = team_stats_df


class Team:
    name = None
    abr = None
    team_stats = None
    opp_stats = None
    misc_stats = None
    adv_player_stats = None
    total_player_stats = None
    boxscores = None

    def __init__(self, name, league):
        self.name = name
        self.abr = NBA_TEAMS.find_NBA_abrev(name)
        self.team_stats, self.opp_stats, self.misc_stats = NBA_WEBSITE_SCRAPPER.get_team_stats(
            name[1], team_stats_df=league.teams_season, misc_stats_df=league.teams_misc, opp_stats_df=league.teams_opp)
        self.adv_player_stats, self.total_player_stats = NBA_WEBSITE_SCRAPPER.get_roster_player_list(self)
        self.boxscores = NBA_WEBSITE_SCRAPPER.set_season_schedule(self.adv_player_stats['slug'])
