import json
import urllib.request
from selenium import webdriver

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('log-level=3')
# driver = webdriver.Chrome(chrome_options=options)
# URL = f"https://www.basketball-reference.com/leagues/NBA_2020.html"
# driver.get(URL)
# html = driver.page_source
# driver.quit()
urlreq = 'https://api.lineups.com/nba/fetch/lineups/current/brooklyn-nets'

response = urllib.request.urlopen(urlreq)

jresponse = json.load(response)
starters = jresponse['starters']

past_lineups = jresponse['past_lineups']
freq_lineups = jresponse['frequent_lineups']

lst_past_lineups = dict()
lst_freq_lineups = dict()
lst_starters = list()

for i in range(5):
    lineup = past_lineups[i]
    result = lineup['result']
    game = str(lineup['game']).split(' vs')
    lst_players = dict()
    for n in range(1, 6):
        name = lineup[str(n)]['name']
        position = lineup[str(n)]['position']
        lst_players.update({name: position})
    lst_past_lineups.update({game[0]: lst_players.items()})

for i in range(5):
    lineup = freq_lineups[i]['players']
    frequency = freq_lineups[i]['frequency']
    lst_players = dict()
    for n in range(5):
        name = lineup[n]['name']
        position = lineup[n]['position']
        lst_players.update({name: position})
    lst_freq_lineups.update({frequency: lst_players.items()})

for i in range(5):
    name = starters[i]['name']
    position = starters[i]['position']
    lst_starters.append({name: position})

print(lst_starters)

for item in lst_freq_lineups.items():
    print(item)



for item in lst_past_lineups.items():
    print(item)
