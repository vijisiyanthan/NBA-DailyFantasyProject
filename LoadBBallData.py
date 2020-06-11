import csv
import sqlite3
import NBA_TEAMS
import datetime
from sys import argv, exit
from NBA_TOOLS import Team
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType


class Matchup():
    opp = None
    home = None

    def __init__(self, opp_team, home_team):
        self.opp = Team(opp_team)
        self.home = Team(home_team)


def get_box_score_date(date):
    if len(date) == 3:
        box_day = date[0]
        box_month = date[1]
        box_year = date[2]
        return box_day, box_month, box_year
    elif date == "":
        box_month = datetime.datetime.now().month
        box_day = datetime.datetime.now().day
        box_year = datetime.datetime.now().year
        return box_day, box_month, box_year
    else:
        print("Invalid Date Format {day/month/year} *numerical values only")
        exit(0)


def get_games_today(day, month, year):
    # need to implement getting games from today's date from basketball reference. For the time being just taking inputs
    # from users
    teams_playing = get_games_from_user()
    for matchup in teams_playing:
        print(matchup.opp.adv_player_stats.head())
        print(matchup.home.adv_player_stats.head())


def get_games_from_user():
    number_games_today = int(input("How many games are played today:"))
    teams_playing = list()
    for game in range(number_games_today):
        print(f"Game {game}:")
        opp = NBA_TEAMS.find_NBA_team(input("Away Team:"))
        home = NBA_TEAMS.find_NBA_team(input("Home Team:"))
        matchup = Matchup(opp, home)
        teams_playing.append(matchup)
    return teams_playing


if __name__ == '__main__':
    if len(argv) == 2:
        day, month, year = get_box_score_date(argv[1].split('/'))
    elif len(argv) == 1:
        day, month, year = get_box_score_date("")
        get_games_today(day, month, year)
