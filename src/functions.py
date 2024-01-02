from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

