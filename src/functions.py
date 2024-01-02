from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from time import sleep

def start_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--headless") # Enable this option when code
    # is working fine to run in headless mode (without opening browser)

    driver = webdriver.Chrome(options=chrome_options)
    url = ""
    driver.get(url)
    return driver

def scraper_main():
    driver = start_chrome()
    #  define actions using subfunctions and selenium here

    driver = get_to_library(driver) # get to the library page

    driver = new_contributor(driver)

    driver = connection_settings(driver)

    driver = processing_steps(driver)

    driver = test_harvest(driver)

    driver = logs(driver)



    driver.close()

def get_to_library(driver):
    collections_path = ""
    collections_box = driver.find_element('css selector', collections_path)
    collections_box.click()
    sleep(0.5)

    anbd_path = ""
    anbd_box = driver.find_element('css selector', anbd_path)
    anbd_box.click()
    sleep(0.5)

    return driver


def new_contributor(driver):
    from_first_path = ""
    from_first_box = driver.find_element('css selector', from_first_path)
    select_from_first = Select(from_first_box)
    from_first_box.click()
    sleep(0.5)

    desired_option = ""
    select_from_first.select_by_visible_text(desired_option)

    # To select by index (0-based index):
    # select_anbd.select_by_index(index)

    # To select by value attribute:
    # select_anbd.select_by_value(value)
    return driver

def connection_settings(driver):
    pass

def data_storage_settings(driver):
    pass

def processing_steps(driver):
    pass

def test_harvest(driver):
    pass

def logs(driver):
    pass