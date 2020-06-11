from basketball_reference_web_scraper import client
import datetime, pytz


players = list(client.player_box_scores(day=1,month=1,year=2020))

schedule = client.season_schedule(season_end_year=2020)

date = datetime.datetime(year=2020,month=3,day=9,tzinfo=pytz.UTC)
for game in schedule:
    #print(f"{game['start_time'].year}")
    if int(game["start_time"].year) == 2020 and int(game["start_time"].month) == 3\
            and int(game["start_time"].day) == 9:
        print("matchhhhhh")
        print(f"{game}")
    # print(game["start_time"])
    # print(date)

# for player in players:
#     print(f'{player["name"]}: {player["made_three_point_field_goals"]}')