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
        "OKLAHOMA_CITY" : "Oklahoma City",
        "PHILADELPHIA_76ERS": "Philadelphia 76ers",
        "PHOENIX_SUNS": "Phoenix Suns",
        "PORTLAND_TRAIL_BLAZERS": "Portland Trail Blazers",
        "SACRAMENTO_KINGS": "Sacramento Kings",
        "SAN_ANTONIO_SPURS": "San Antonio Spurs",
        "TORONTO_RAPTORS": "Toronto Raptors",
        "UTAH_JAZZ": "Utah Jazz",
        "WASHINGTON_WIZARDS": "Washington Wizards",
    }
    abbreviations = {
        "ATL": "Atlanta Hawks",
        "BOS": "Boston Celtics",
        "BKN": "Brooklyn Nets",
        "CHA": "Charlotte Hornets",
        "CHI": "Chicago Bulls",
        "CLE": "Cleveland Cavaliers",
        "DAL": "Dallas Mavericks",
        "DEN": "Denver Nuggets",
        "DET": "Detroit Pistons",
        "GS": "Golden State Warriors",
        "HOU": "Houston Rockets",
        "IND": "Indiana Pacers",
        "LAC": "Los Angeles Clippers",
        "LAL": "Los Angeles Lakers",
        "MEM": "Memphis Grizzlies",
        "MIA": "Miami Heat",
        "MIL": "Milwaukee Bucks",
        "MIN": "Minnesota Timberwolves",
        "NOP": "New Orleans Pelicans",
        "NY": "New York Knicks",
        "ORL": "Orlando Magic",
        "OKC": "Oklahoma City",
        "PHI": "Philadelphia 76ers",
        "PHO": "Phoenix Suns",
        "POR": "Portland Trail Blazers",
        "SAC": "Sacramento Kings",
        "SA": "San Antonio Spurs",
        "TOR": "Toronto Raptors",
        "UTA": "Utah Jazz",
        "WAS": "Washington Wizards",
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


def find_NBA_abrev(input):
    names = NBA_TEAMS.abbreviations
    team = ""
    for name in names.items():
        if input == name[0]:
            team = name[1]

    if team == "":
        print("Team Not Found!!!")
        exit(0)
    else:
        return team.upper()

def get_NBA_abrev(input):
    names = NBA_TEAMS.abbreviations
    team = ""
    for name in names.items():
        if input == name[1].upper():
            team = name[0]

    if team == "":
        print("Team Not Found!!!")
        exit(0)
    else:
        return team
