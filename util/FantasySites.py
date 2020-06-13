class FantasySites:
    FanDuel = {"scoring": 1,
               "rebound": 1.2,
               "assist": 1.5,
               "block": 3,
               "steal": 3,
               "turnover": -1
               }

    sites = {
        "FanDuel": FanDuel
    }


def calculate_fantasy_value(boxscore, fantasy_site):
    selected_site = FantasySites.sites[fantasy_site]
    fantasyvalue = boxscore['points_scored'] * selected_site['scoring'] + \
                   boxscore['steals'] * selected_site['steal'] + \
                   boxscore['blocks'] * selected_site['block'] + \
                   boxscore['defensive_rebounds'] * selected_site['rebound'] + \
                   boxscore['offensive_rebounds'] * selected_site['rebound'] - \
                   boxscore['turnovers'] * selected_site['turnover']
    return fantasyvalue
