from basketball_reference_web_scraper import client
from sys import argv
import datetime
from util.FantasySites import FantasySites
from util import FantasySites


## Find player matchup history vs opponent
def get_player_boxscores(starting_year, year_range, player):
    player_avg = 0
    total_games_vs_opp = 0
    for val in range(year_range):
        try:
            boxscores = client.regular_season_player_box_scores(
                player_identifier=play['identifier'],
                season_end_year=starting_year + val,
            )
        except client.InvalidPlayerAndSeason:
            continue

        for game in boxscores:
            if game['opponent'].name == opp:
                player_avg += FantasySites.calculate_fantasy_value(game, fantasy_site)
                total_games_vs_opp += 1

    return player_avg / total_games_vs_opp, total_games_vs_opp


def find_players(player_name):
    return client.search(term=player_name)["players"]


if __name__ == '__main__':
    if len(argv) == 5:
        fantasy_site = input("Enter Fantasy Site: ")
        name = f"{argv[1]} {argv[2]}"
        opp = f"{argv[3]}"
        start_year = int(argv[4])
        year_range = datetime.datetime.now().year - start_year
        players = find_players(name)
        for play in players:
            print(play['identifier'])
            player_avg, total_games = get_player_boxscores(starting_year=start_year, year_range=year_range, player=play)

        print(
            f"Player Average vs {opp} in {total_games} Games: {player_avg} on {fantasy_site}")
    else:
        print("Invalid Usage: vsTeam.py {player name} {opponent name} {starting year}")
