import LoadBBallData
from FANTASY_DATABASE import FantasyDatabase
from sys import argv

if __name__ == '__main__':
    if len(argv) == 2 and argv[1] == "load":
        LoadBBallData.get_games_today()
    elif len(argv) == 1:
        bball_db = FantasyDatabase()
        print(bball_db.boxscores.head())
    else:
        print("Usage: python main.py {load} *optional")
        exit(0)
