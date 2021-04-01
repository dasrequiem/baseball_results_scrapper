from results_scrapper import getChromeDriver, downloadGameResults, getMatchLinks, make_csv_file


if __name__ == '__main__':
    # Driver configuration variables
    DOWNLOAD_FOLDER = './pdf/'
    DRIVER_FOLDER = '/Users/aruki/code/chromedriver'
    RESULTS_URL = 'https://fedebeis.com.pa/boxscore-juvenil-2020/'
    CSV_NAME = 'results_minor_league_2020.csv'

    driver = getChromeDriver(DRIVER_FOLDER, DOWNLOAD_FOLDER)

    driver.get(RESULTS_URL)

    # we get the Game links
    partidos = getMatchLinks(driver)

    # download the pdf files
    partidos = downloadGameResults(driver, partidos)

    # make a csv file with the gathered links
    make_csv_file(partidos, 'results_minor_league_2020.csv', True)

    driver.quit()
