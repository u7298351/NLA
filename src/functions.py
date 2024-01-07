from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
from time import sleep


# Example usage
max_iterations = 10  # Set this to control the number of iterations
scraper_main(max_iterations)



def scraper_main(max_iterations):
    driver = start_chrome()
    driver = collect_Input_GUI_And_CSVDetails(driver, max_iterations)
    driver.close()


def start_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--headless") # Enable this option when code
    # is working fine to run in headless mode (without opening browser)

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def collect_Input_GUI_And_CSVDetails(driver, numberOfIterations):
   def collect_Input_GUI_And_CSVDetails(driver, max_iterations):
    with open('your_file.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if there is one

        for i, row in enumerate(csv_reader):
            if i >= max_iterations:
                break  # Stop the loop if max_iterations is reached

            data = row[0]  # Extract data from the first column

            url = "https://ourweb.nla.gov.au/HarvesterClient/ListCollections.htm"
            driver.get(url)

            try:
                link_xpath = f"//a[contains(text(), '{data}')]"
                link = driver.find_element(By.XPATH, link_xpath)
                link.click()
                sleep(1)  # Wait for page to load after click
            except Exception as e:
                print(f"Error finding link for {data}: {e}")

            driver = copyContributorVariables(driver, data)
            driver = create_new_contributor(driver, data)
    
    return driver


def copyContributorVariables(driver):
    # need to copy the variables from the contributor page
    # need to paste the variables into the new contributor page
    # Extract the value from the first textbox

    editContributor = driver.find_element(By.CSS_SELECTOR, "#content > ul > li:nth-child(1) > a")
    editContributorvalue = editContributor.click("value")
    sleep(0.5)

    contributorName = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(2) > input[type=text]")
    contributorNamevalue = contributorName.get_attribute("value")
    

    description = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(4) > input[type=text]")
    descriptionvalue = description.get_attribute("value")
    
    
    platform = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(10) > input[type=text]")
    platformvalue = platform.get_attribute("value")

    
    orgID = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(12) > input[type=text]")
    orgIDvalue = orgID.get_attribute("value")

    
    
# need to confirm all of the selectors are right - mightve screwed it
    #  = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(10) > input[type=text]")
    # contributorNamevalue = contributorName.get_attribute("value")
    input_element.send_keys(Keys.TAB)
    input_element.send_keys("s")
    input_element.send_keys(Keys.TAB)

    contactName = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > table > tbody > tr:nth-child(4) > td:nth-child(1) > input")
    contactNamevalue = contactName.get_attribute("value")
    contactEmail = driver.find_element(By.CSS_SELECTOR, "   #contributorform > fieldset > table > tbody > tr:nth-child(4) > td:nth-child(3) > input")
    contactEmailvalue = contactEmail.get_attribute("value")
    #contributorform > fieldset > table > tbody > tr:nth-child(4) > td:nth-child(3) > input
    return driver


def create_new_contributor(driver):
    driver = openANBSCollection(driver)
    driver = openANBDCollection(driver)
    driver = createNewContributor(driver)
    driver = inputContributorDetails
    driver = save(driver)
    driver = inputConnectionDetails
    driver = save(driver)
    driver = inputDataStoreSettings
    driver = save(driver)
    driver = editProcessingSteps(driver)
    driver = save(driver)
    driver = runTestHarvest(driver)
    driver = downloadLogs(driver)
    driver 

    anbs_path = "#content > table > tbody > tr:nth-child(14) > td:nth-child(1) > a"
    anbs_box = driver.find_element('css selector', anbs_path)
    anbs_box.click()
    sleep(0.5)
    
    anbs_addnew = "#content > ul > li > a"
    anbs_addnew_box = driver.find_element('css selector', anbs_addnew)
    anbs_addnew_box.click()
    sleep(0.5)


    name_insert = "#contributorform > fieldset > dl > dd:nth-child(2) > input[type=text]"
    input_element = driver.find_element('css selector', name_insert)
    input_element.send_keys("Name VARIABLE INSERTION" )
    input_element.send_keys(Keys.TAB)
    input_element.send_keys("Description VARIABLE INSERTION" )
    input_element.send_keys(Keys.TAB)
    input_element.send_keys("Platform VARIABLE INSERTION" )
    input_element.send_keys(Keys.TAB)
    input_element.send_keys("org ID VARIABLE INSERTION" )
    input_element.send_keys(Keys.TAB)
    input_element.send_keys("s" )
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.ENTER)
    input_element.send_keys(Keys.TAB)
    #need an if to check if there are contributors
    input_element.send_keys("Contributor Name VARIABLE INSERTION" )
    input_element.send_keys(Keys.TAB)
    input_element.send_keys("Job title VARIABLE INSERTION" )
    input_element.send_keys(Keys.TAB)
    input_element.send_keys("Email VARIABLE INSERTION" )
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    #need logic here to handle T or B typing based on box
    #need an if to check if there are morecontributors
    input_element.send_keys("Contributor Name VARIABLE INSERTION" )
    #need an if to check if there are contributors
    

    setConnectionPath = "#mainsubmit"
    setConnectionBox = driver.find_element('css selector', setConnectionPath)
    setConnectionBox.click()
    sleep(0.5)

    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    
    urlPath = "#settingsform > fieldset > dl > dd:nth-child(6) > input"
    urlPathBox = driver.find_element('css selector', urlPath)
    urlPathBox = driver.send_keys("URL VARIABLE")


    saveConnectionSettings = "#settingsform > ul > li:nth-child(3) > a"
    saveConnectionSettingsBox = driver.find_element('css selector', saveConnectionSettings)
    saveConnectionSettingsBox.click()
    sleep(0.5)

#save connection settings box
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.ENTER)


    setInsert = "#settingsform > fieldset > dl > dd:nth-child(8) > input[type=text]"
    setInsertBox = driver.find_element('css selector', setInsert)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    # input_element.send_keys(Keys.TAB)
    urlInsertBox = driver.send_keys("SET VARIABLE")
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.BACKSPACE)
    input_element.send_keys(Keys.BACKSPACE)
    input_element.send_keys(Keys.BACKSPACE)
    input_element.send_keys(Keys.BACKSPACE)
    input_element.send_keys(Keys.BACKSPACE)
    input_element.send_keys(Keys.BACKSPACE)
    input_element.send_keys("marc21")
    
    # urlInsertBox = driver.send_keys("SET VARIABLE")
    # urlInsertBox = driver.send_keys("marcXML") #this needs correcting!
    input_element.send_keys(Keys.TAB)
    urlInsertBox = driver.send_keys("500")
    input_element.send_keys(Keys.TAB)
    #below will need logic for the SirsiDynix Platforms
    input_element = driver.send_keys("Platform VARIABLE")
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.Enter)
    sleep(0.5)

    #edit DataStore Settings
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)    
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)    
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.Enter) #not sure if it is meant to be an enter here, or if it is the correct number
    sleep(0.5)

    #insert NUC 
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)    
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)    
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys("NUC VARIABLE")
    # Save DataStore
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.ENTER)
    sleep(0.5)

    # Edit Processing Steps
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    sleep(0.5)

    # edit test steps
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    sleep(0.5)
    
    
    editNucStep = "#ProcessingStepsForm > table > tbody > tr:nth-child(11) > td:nth-child(8) > ul > li:nth-child(1) > a"
    editNucStepBox = driver.find_element('css selector', editNucStep)
    editNucStepBox.click()
    sleep(0.5)

    insertNUCText = "#processingstepform > dl > dd:nth-child(16) > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr.clone > td:nth-child(2) > input"
    insertNUCTextbox = driver.find_element('css selector', insertNUCText)
    insertNUCTextbox.click()
    sleep(0.5)
   
    replaceCHANGE = "#processingstepform > dl > dd:nth-child(12) > input[type=text]"
    replaceCHANGEbox = driver.find_element('css selector', replaceCHANGE)
    replaceCHANGEbox.click()
    sleep(0.5)
   
    saveNuc = "#mainsubmit"
    saveNucbox = driver.find_element('css selector', saveNuc)
    saveNucbox.click()
    sleep(0.5)
    
    
    saveSteps = "#ProcessingStepsForm > ul:nth-child(5) > li:nth-child(2) > input"
    saveStepsbox = driver.find_element('css selector', saveSteps)
    saveStepsbox.click()
    sleep(0.5)

    performTestHarvest = "#subnav > li:nth-child(5) > a"
    performTestHarvestbox = driver.find_element('css selector', performTestHarvest)
    performTestHarvestbox.click()
    sleep(0.5)
    
    
    fiftyRecords = "#manual > dd:nth-child(6) > dl > dd:nth-child(5) > input:nth-child(6)"
    fiftyRecordsbox = driver.find_element('css selector', fiftyRecords)
    fiftyRecordsbox.click()
    sleep(0.5)


    harvest = "#mainsubmit"
    harvestbox = driver.find_element('css selector', harvest)
    harvestbox.click()
    sleep(0.5)

    
    logs = "#subnav > li.on > a"
    logsbox = driver.find_element('css selector', logs)
    logsbox.click()
    sleep(0.5)


    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.TAB)
    input_element.send_keys(Keys.ENTER)
    
    downloadAll = "#content > dl:nth-child(3) > dd:nth-child(9) > ul > li:nth-child(3) > a"
    downloadAllbox = driver.find_element('css selector', downloadAll)
    downloadAllbox.click()
    sleep(0.5)

    return driver




    