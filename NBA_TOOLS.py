import NBA_TEAMS
import NBA_WEBSITE_SCRAPPER


class Team:
    name = None
    abr = None
    team_stats = None
    opp_stats = None
    misc_stats = None
    adv_player_stats = None
    total_player_stats = None

    def __init__(self, name):
        self.name = name
        self.abr = NBA_TEAMS.find_NBA_abrev(name)
        self.team_stats, self.opp_stats, self.misc_stats = NBA_WEBSITE_SCRAPPER.get_team_stats(name[1])
        self.adv_player_stats, self.total_player_stats = NBA_WEBSITE_SCRAPPER.get_roster_player_list(self)
