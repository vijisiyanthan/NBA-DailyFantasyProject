import LoadBBallData
from FANTASY_DATABASE import FantasyDatabase
from sys import argv


def set_players_per_gamestats():
    player_stats = bball_db.player_stats


def set_players_not_playing():
    name = ""
    teams = bball_db.player_stats['team'].unique()
    print(f"Teams playing:")
    for team in teams:
        print(team)
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


if __name__ == '__main__':
    if len(argv) == 2 and argv[1] == "load":
        LoadBBallData.get_games_today()
    elif len(argv) == 1:
        bball_db = FantasyDatabase()
        set_players_not_playing()

        print((bball_db.team_stats.dtypes))
        # for team in bball_db.lineups.keys():
        #     print(f"{team}:{list(bball_db.lineups[team].freq.values())[0]}")
    else:
        print("Usage: python main.py {load} *optional")
        exit(0)
