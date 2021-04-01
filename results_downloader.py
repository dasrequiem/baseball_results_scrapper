from results_scrapper import downloadGameResults, getChromeDriver
import csv
from game import Game


def download_results(links):
    driver = getChromeDriver()
    downloadGameResults(driver, links)


if __name__ == '__main__':
    FILE = 'results_minor_league_2020.csv'
    match_list = []

    with open(FILE, 'r') as f:
        rows = csv.DictReader(f, delimiter=',')

        # fields: match,result_link,download_link,downloaded
        for r in rows:
            downloaded = (r['downloaded'].lower() == 'true')
            if not(downloaded):
                match = Game(r['match'], r['result_link'],
                             r['download_link'], r['downloaded'])
                match_list.append(match)

    if len(match_list) > 0:
        download_results(match_list)
