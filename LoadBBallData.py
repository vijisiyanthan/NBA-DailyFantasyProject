import sqlite3
import NBA_TEAMS
import datetime
from sys import argv, exit
from NBA_TOOLS import Team
from NBA_TOOLS import League

league = League()


class Matchup():
    opp = None
    home = None

    def __init__(self, opp_team, home_team, league):
        self.opp = Team(opp_team, league)
        self.home = Team(home_team, league)


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


def get_games_today():
    # need to implement getting games from today's date from basketball reference. For the time being just taking inputs
    # from users
    teams_playing = get_games_from_user()
    conn = sqlite3.connect("fantasy.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS players_adv_stats;")
    cur.execute("DROP TABLE IF EXISTS players_total_stats;")
    cur.execute("DROP TABLE IF EXISTS misc_stats;")
    cur.execute("DROP TABLE IF EXISTS player_boxscores;")
    cur.execute("DROP TABLE IF EXISTS matchups;")

    cur.execute("CREATE TABLE matchups(home_team,away_team);")

    matchups_list = dict()
    for matchup in teams_playing:
        cur.execute("INSERT INTO matchups(home_team,away_team) VALUES (?,?);",
                    [matchup.home.name[1], matchup.opp.name[1]])
        matchups_list.update({matchup.home.name[1]: matchup.opp.name[1]})
        matchup.opp.adv_player_stats.to_sql('players_adv_stats', con=conn, if_exists='append', chunksize=1000)
        matchup.home.adv_player_stats.to_sql('players_adv_stats', con=conn, if_exists='append', chunksize=1000)

        matchup.opp.total_player_stats.to_sql('players_total_stats', con=conn, if_exists='append', chunksize=1000)
        matchup.home.total_player_stats.to_sql('players_total_stats', con=conn, if_exists='append', chunksize=1000)

        # matchup.opp.misc_stats.to_sql('misc_stats', con=conn, if_exists='append', chunksize=1000)
        # matchup.home.misc_stats.to_sql('misc_stats', con=conn, if_exists='append', chunksize=1000)

        matchup.home.boxscores.to_sql('player_boxscores', con=conn, if_exists='append', chunksize=1000)
        matchup.opp.boxscores.to_sql('player_boxscores', con=conn, if_exists='append', chunksize=1000)

    league.teams_misc.to_sql('misc_stats', con=conn, if_exists='append', chunksize=1000)
    return matchups_list


def get_games_from_user():
    number_games_today = int(input("How many games are played today:"))
    teams_playing = list()
    for game in range(number_games_today):
        print(f"Game {game}:")
        opp = NBA_TEAMS.find_NBA_team(input("Away Team:"))
        home = NBA_TEAMS.find_NBA_team(input("Home Team:"))
        matchup = Matchup(opp, home, league)
        teams_playing.append(matchup)
    return teams_playing
