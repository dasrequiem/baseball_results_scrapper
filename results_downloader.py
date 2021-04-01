from results_scrapper import downloadGameResults
import csv
from game import game

if __name__ == '__main__':
    FILE = 'results_minor_league_2020.csv'

    with open(FILE, 'r') as f:
        results = csv.DictReader(f, delimiter=',')

        for r in results:
            downloaded = (r['downloaded'].lower() == 'true')
