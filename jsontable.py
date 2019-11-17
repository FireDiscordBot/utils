import json
from bs4 import BeautifulSoup

def table2json(table, keys: list):
    soup = BeautifulSoup(table, "html.parser")
    leaderboard = []
    for row in soup.find_all('tr'):
        values = [td.get_text(strip=True) for td in row.find_all('td')]
        row = dict(zip(keys, values))
        leaderboard.append(row)
    return leaderboard
