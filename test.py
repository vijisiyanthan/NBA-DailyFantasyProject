import json
import urllib.request
from selenium import webdriver
from pydfs_lineup_optimizer import get_optimizer, Site, Sport, Player
import pandas as pd

fanduel_sheet = pd.read_csv("fanduel.csv")
players_names = list(fanduel_sheet['Nickname'])
print(players_names)

