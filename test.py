from basketball_reference_web_scraper import client


players = list(client.player_box_scores(day=1,month=1,year=2020))

schedule = client.season_schedule(season_end_year=2020)

print(schedule)

for game in schedule:
    print(game)
    print()

# for player in players:
#     print(f'{player["name"]}: {player["made_three_point_field_goals"]}')