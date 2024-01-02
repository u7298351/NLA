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



    driver.close()

def get_to_library():
    

