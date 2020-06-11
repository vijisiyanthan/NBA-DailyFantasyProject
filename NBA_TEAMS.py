class NBA_TEAMS:
    names = {
        "ATLANTA_HAWKS": "Atlanta Hawks",
        "BOSTON_CELTICS": "Boston Celtics",
        "BROOKLYN_NETS": "Brooklyn Nets",
        "CHARLOTTE_HORNETS": "Charlotte Hornets",
        "CHICAGO_BULLS": "Chicago Bulls",
        "CLEVELAND_CAVALIERS": "Cleveland Cavaliers",
        "DALLAS_MAVERICKS": "Dallas Mavericks",
        "DENVER_NUGGETS": "Denver Nuggets",
        "DETROIT_PISTONS": "Detroit Pistons",
        "GOLDEN_STATE_WARRIORS": "Golden State Warriors",
        "HOUSTON_ROCKETS": "Houston Rockets",
        "INDIANA_PACERS": "Indiana Pacers",
        "LOS_ANGELES_CLIPPERS": "Los Angeles Clippers",
        "LOS_ANGELES_LAKERS": "Los Angeles Lakers",
        "MEMPHIS_GRIZZLIES": "Memphis Grizzlies",
        "MIAMI_HEAT": "Miami Heat",
        "MILWAUKEE_BUCKS": "Milwaukee Bucks",
        "MINNESOTA_TIMBERWOLVES": "Minnesota Timberwolves",
        "NEW_ORLEANS_PELICANS": "New Orleans Pelicans",
        "NEW_YORK_KNICKS": "New York Knicks",
        "ORLANDO_MAGIC": "Orlando Magic",
        "PHILADELPHIA_76ERS": "Philadelphia 76ers",
        "PHOENIX_SUNS": "Phoenix Suns",
        "PORTLAND_TRAIL_BLAZERS": "Portland Trail Blazers",
        "SACRAMENTO_KINGS": "Sacramento Kings",
        "SAN_ANTONIO_SPURS": "San Antonio Spurs",
        "TORONTO_RAPTORS": "Toronto Raptors",
        "UTAH_JAZZ": "Utah Jazz",
        "WASHINGTON_WIZARDS": "Washington Wizards",
    }


def find_NBA_team(user_input):
    names = NBA_TEAMS.names
    team = ""
    for name in names.items():
        if user_input.lower() in name[1].lower():
            team = name

    if team == "":
        print("Team Not Found!!!")
        exit(0)
    else:
        print(team)
        return team


if __name__ == '__main__':
    find_NBA_team(input("Enter Team:"))
