from basketball_reference_web_scraper import client
from sys import argv
from fantasysites import FantasySites
import fantasysites

## Find player matchup history vs opponent


if __name__ == '__main__':
    if len(argv) == 4:
        fantasy_site = input("Enter Fantasy Site: ")
        name = f"{argv[1]} {argv[2]}"
        opp = f"{argv[3]}"
        player = client.search(term=name)
        players = player["players"]
        for play in players:
            print(play['identifier'])
            for i in range(10):
                boxscores = client.regular_season_player_box_scores(
                    player_identifier=play['identifier'],
                    season_end_year=2010 + i,
                )
                for game in boxscores:
                    if game['opponent'].name == opp:
                        print(fantasysites.calculate_fantasy_value(game, fantasy_site))
