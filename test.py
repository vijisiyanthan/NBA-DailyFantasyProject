from basketball_reference_web_scraper import client
import datetime, pytz

from basketball_reference_web_scraper.data import OutputType

players = list(client.player_box_scores(day=1,month=1,year=2020))

client.season_schedule(season_end_year=2020, output_type=OutputType.CSV, output_file_path="./2019_2020_season.csv")

# Output all player box scores for January 1st, 2017 in JSON format to 1_1_2017_box_scores.csv
client.regular_season_player_box_scores(player_identifier="westbru01",season_end_year=2020 ,output_type=OutputType.CSV, output_file_path="./1_1_2017_box_scores.csv")

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


   # options = webdriver.ChromeOptions()
   #  options.add_argument('--headless')
   #  options.add_argument('log-level=3')
   #  driver = webdriver.Chrome(chrome_options=options)
   #  URL = f"https://www.basketball-reference.com/teams/{team.abr}/2020.html"
   #  driver.get(URL)
   #  html = driver.page_source
   #  driver.quit()
   #
   #  soup = BeautifulSoup(html, 'html.parser')
   #  team_roster_div = soup.find(id="all_roster")
   #  team_roster_table = team_roster_div.find(id="roster")
   #
   #  df_list = pd.read_html(str(team_roster_table))
   #  team_roster_df = df_list[0]
   #  team_roster_df = team_roster_df.drop(columns=['No.', 'Ht', 'Wt', 'Birth Date', 'Unnamed: 6', 'Exp', 'College'])
   #  team_roster_tuple = list(team_roster_df.itertuples(index=False, name=None))