from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from game import game
import traceback
import time

# Driver configuration variables
DOWNLOAD_FOLDER = './pdf/'
DRIVER_FOLDER = '/Users/aruki/code/chromedriver'
RESULTS_URL = 'https://fedebeis.com.pa/boxscore-juvenil-2020/'
CSV_NAME = 'results.csv'

# dump the list of games and download links to a csv file


def make_csv_file(results, file=CSV_NAME, echo=False):
    with open(file, 'a') as f:
        headers = 'match, result_link, download_link\n'
        if echo:
            print(headers + '\n')
        f.write(headers)

        for result in results:
            line = result.getValuesCSV() + '\n'
            if echo:
                print(line)
            f.write(line)


# chrome options for download
prefs = {
    "download.default_directory": DOWNLOAD_FOLDER,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True,
}
chrome_options = Options()
chrome_options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(DRIVER_FOLDER, options=chrome_options)
driver.get(RESULTS_URL)

# find the button for next pagination
next_button = driver.find_element_by_xpath(
    "//*[@id='tie-block_2186']/div/div[1]/div/div/ul/li[2]/a")
# results = driver.find_elements_by_xpath("//li/h3/a")
# print('cantidad de resultados: {}'.format(len(results)))
partidos = []
loop = True
cont = 1

# loop the results
while loop:
    wait = WebDriverWait(driver, 10)
    next_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'next-posts')))

    # next_button = driver.find_element_by_class_name('next-posts')
    loop = not ('pagination-disabled' in next_button.get_attribute('class'))
    #print(next_button.get_attribute('class') + ' | ' + str(loop))

    results = driver.find_elements_by_xpath("//li/h3/a")
    print(' {} results in page {} !'.format(str(len(results)), cont))

    for result in results:
        partido = game(result.text, result.get_attribute('href'))
        partidos.append(partido)

    if loop:
        next_button.click()
        # wait for the transition animation to finish loading results
        time.sleep(6)
        driver.implicitly_wait(6)

    cont += 1

print('Games to download: {}'.format(len(partidos)))
cont = 1
total = len(partidos)

# we loop through the gathered download links
for partido in partidos:
    print('Downloading game result {}/{} {}'.format(str(cont),
          str(total), partido.titulo))
    cont += 1
    driver.get(partido.link)
    time.sleep(2)
    # if not ('P.Pospuesto' in partido.titulo):
    try:
        download = driver.find_element_by_class_name('s_pdf_download_link')
        partido.download_link = download.get_attribute('href')
        driver.get(download.get_attribute('href'))
    except:
        partido.download_link = ''
        print('Encountered an issue downloading results for {}'.format(partido.titulo))
        # traceback.print_exc()

make_csv_file(partidos, 'results_minor_league_2020.csv', True)

driver.quit()
