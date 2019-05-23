import json
from bs4 import BeautifulSoup

def table2json(table):
    soup = BeautifulSoup(table, "lxml")
    leaderboard = []
    for row in soup.find_all('tr'):
        keys = ['Position', 'Change', 'Name', 'Level', 'Karma', 'Total Wins', 'Total Kills']
        values = [td.get_text(strip=True) for td in row.find_all('td')]
        row = dict(zip(keys, values))
        leaderboard.append(row)
    return leaderboard