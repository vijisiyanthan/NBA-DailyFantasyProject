import NBA_TEAMS
import NBA_WEBSITE_SCRAPPER


class Team:
    name = None
    team_stats = None
    opp_stats = None
    misc_stats = None

    def __init__(self, name):
        self.name = name
        self.team_stats, self.opp_stats, self.misc_stats = NBA_WEBSITE_SCRAPPER.get_team_stats(name[1])
