from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import tkinter as tk
import csv
import re
import os
import subprocess
from time import sleep
import shutil
from selenium.common.exceptions import NoSuchElementException

#need to check logic for - platform sirsi
#need to check logic for - variable storing
#need to check logic for - description insertion - may not matter
#need to check logic for - notes - we can add it as we see it
#need to check logic for finding the correct test processing step
#building on prior one - need check specific libero logic for each harvesting profile 0 including extracting it if libero

#need seperate code for running put in active contributor section
#Idea - could add logic to check for unique XSLT sheets from the standards - and spit those out into another csv list to be consulted with later - would be helpful with universities
#need code to check if it is custom setup

#need check marcedit file conversion
#need finish gui for general harvester creation
#need code to deal with contributor type dropdown - variable and insert.
#TODO to do add code to go back to connection settings, switch contributor notifications on for anbd and anbs <-- need to figure out if I want to do this or not

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
def remove_square_brackets(name):
    # Remove only the square brackets, keep the content inside
    return re.sub(r'[\[\]]', '', name)
def clean_formatting(name):
    # Convert to bytes and then decode to ignore non-UTF characters
    name = name.encode('utf-8', 'ignore').decode('utf-8', 'ignore')

    # Remove specific unwanted characters
    characters_to_remove = ['ï', '»', '¿']
    for char in characters_to_remove:
        name = name.replace(char, '')

    # Replace invalid file path characters with a single space
    cleaned_name = re.sub(r'[:/\\|*?"<>]', ' ', name)

    # Additional cleaning to ensure no consecutive spaces
    cleaned_name = ' '.join(cleaned_name.split())

    return cleaned_name
def collect_Input_GUI_And_CSVDetails(driver, username, password, contributorNamevalue):
    print("1")
    url = "https://ourweb.nla.gov.au/HarvesterClient/ListCollections.htm"
    driver.get(url)
    sleep(5)
    
    print("2")
    driver.find_element(By.CSS_SELECTOR, "#username").send_keys(username)
    print("3")
    sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
    print("4")
    sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, "#kc-login").click()
    sleep(1)
    print("5")
    print("inputting anbd finder")
    anbd_path = "#content > table > tbody > tr:nth-child(5) > td:nth-child(1) > a"
    anbd_box = driver.find_element(By.CSS_SELECTOR, anbd_path)
    anbd_box.click()
    sleep(0.5)
    print("went to anbd collection")
    print(contributorNamevalue)
    contributorNamevalue = clean_contributor_name1(remove_square_brackets(contributorNamevalue))
    contributorNuc = get_letters_before_space(contributorNamevalue)
    print("got to i dont know where")
    try:
        link_xpath = f"//a[contains(text(), '{contributorNuc}')]"
        print("found "+ contributorNuc)
        link = driver.find_element(By.XPATH, link_xpath)
        link.click()
        sleep(0.5)  # Wait for page to load after click
    except Exception as e:
        print(f"Error finding link for {contributorNuc}: {e}")

    print("Found contributor")
    return driver
def get_letters_before_space(text):
    match = re.search(r'^\S+', text)
    if match:
        return match.group()
    else:
        return None
# Example callback function
def print_message(message):
    print(message)

def clean_contributor_name1(name):
    # Convert to bytes and then decode to ignore non-UTF characters
    name = name.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
    # Replace invalid file path characters with a single space
    cleaned_name = re.sub(r'[\[\]:/\\|*?"<>]', ' ', name)
    # Additional cleaning to ensure no consecutive spaces
    cleaned_name = ' '.join(cleaned_name.split())

    # Remove specific unwanted characters
    characters_to_remove = ['ï', '»', '¿']
    for char in characters_to_remove:
        cleaned_name = cleaned_name.replace(char, '')

    return cleaned_name
# Test the function with the callback
def scraper_main(max_iterations, csv_file_path, update_gui_callback, username, password):
    print("Got to scraper_main")
    base_download_folder = r"C:\Users\lknoke\Downloads\NLA\HarvesterANBDtoANBS"
    print("6")
    # Initialize the WebDriver
    print("7")
    with open(csv_file_path, 'r') as file:
        print("8.5")
        csv_reader = csv.reader(file)
        
        print("9.5")
        for i, row in enumerate(csv_reader):
            if i >= max_iterations:
                break
            print("11")
            contributorNamevalue = row[0]  # Assuming the contributorNamevalue is in the first column
            print(contributorNamevalue)
            print(remove_square_brackets(clean_formatting(contributorNamevalue)))
            contributorNamevalue = remove_square_brackets(clean_formatting(contributorNamevalue))
            update_gui_callback(f"Processing row {i+1}: {contributorNamevalue}")
            print("10")
            # Set up the download folder for each contributor
            download_folder = create_download_folder(base_download_folder, contributorNamevalue)
            print(f"Created folder for {contributorNamevalue}")
            print("8")
            # Start Chrome with the download path set
            driver = start_chrome_with_download_path(download_folder)
            update_gui_callback("Chrome started with download path set.")
            print("9")
            # Collect input details
            driver = collect_Input_GUI_And_CSVDetails(driver, username, password, contributorNamevalue)
            print("Collected input details")

            print("collectedInputDetails")
            driver, contributorNamevalue, contributorNUCvalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue, urlTakervalue, setTakervalue, contributors = copyContributorVariables(driver, contributorNamevalue)
            print("collectedcontributorvariables")
            driver = create_new_contributor(driver, contributorNamevalue, contributorNUCvalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue, urlTakervalue, setTakervalue, contributors)
            print("createdNewContributor")

            update_gui_callback(f"Row {i+1} processed successfully.")
            sleep(2)  # Adjust sleep as needed

        # Close the driver after processing each row
        update_gui_callback("Scraping completed.")
        driver.close()

    
    update_gui_callback("Scraping completed completed.")

def extract_contributor_NUC(contributorNamevalue):
    try:
        # Regular expression to find all characters up to the first space
        match = re.search(r'(\S+)', contributorNamevalue)
        if match:
            # Extract the value up to the first space
            contributorNUCvalue = match.group(1)
            return contributorNUCvalue
        else:
            # Handle cases where no match is found
            raise ValueError("No NUC value found in the contributor name.")

    except Exception as error:
        # Handle any unexpected errors
        print(f"Error occurred: {error}")
        return None

def start_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--safebrowsing-disable-download-protection')
    chrome_options.add_argument('--safebrowsing-disable-extension-blacklist')
    # chrome_options.add_argument("--headless") # Enable this option when code
    # is working fine to run in headless mode (without opening browser)

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def start_chrome_with_download_path(download_path):
    print("got to chrome start function")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    prefs = {"download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
            }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    sleep(5)
    return driver

def process_csv_data(driver, max_iterations, contributorNamevalue):
    with open('your_file.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if there is one

        for i, row in enumerate(csv_reader):
            if i >= max_iterations:
                break


            data = row[0]
            driver = collect_Input_GUI_And_CSVDetails(driver, data)
            print("collectedInputDetails")
            driver, ticked_checkboxes, contributorNamevalue, contributorNUCvalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue, urlTakervalue, setTakervalue, contributors = copyContributorVariables(driver, contributorNamevalue)
            print("collectedcontributorvariables")
            driver = create_new_contributor(driver, ticked_checkboxes, contributorNamevalue, contributorNUCvalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue, urlTakervalue, setTakervalue, contributors)
            print("createdNewContributor")
    return driver


def copyContributorVariables(driver, contributorNamevalue):
    # Ensure all functions are called in the correct order
    # Extract variables from the contributor page
    "going to contributorVariables function now"

    driver, ticked_checkboxes, contributorNUCvalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue = contributorVariables(driver, contributorNamevalue)
    print("copied contributor setup details")
    # Process contributor details

    driver, contributors = contributorDetailsVariables(driver)
    print("copied contributor details")

    driver, urlTakervalue, setTakervalue = connectionSettingsVariables(driver)
    print("copied contributor connection settings")

    if platformValue.lower() == "libero":
        driver, liberoFieldName, liberoRequiredvalue = liberoSetExtractor(driver)
    else :
        liberoFieldName = None
    # Run test harvest
    driver = runTestHarvest(driver)
    print("ran test harvest")

    # Download logs and old sheet for comparison
    driver = logsDownloadOldSheetForComparison(driver, contributorNamevalue)
    print("downloaded logs of original harvest")

    return driver,  ticked_checkboxes, liberoFieldName, liberoRequiredvalue, contributorNUCvalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue, urlTakervalue, setTakervalue, contributors

def check_and_untick_checkboxes(driver):
    ticked_checkboxes = []
    row = 4  # Starting from row 4 as per your example

    while True:
        for col in range(5, 8):  # Columns 5 to 7
            try:
                checkbox_selector = f"#contributorform > fieldset > table > tbody > tr:nth-child({row}) > td:nth-child({col}) > input[type=checkbox]"
                checkbox = driver.find_element_by_css_selector(checkbox_selector)

                if checkbox.is_selected():
                    ticked_checkboxes.append((row, col))
                    checkbox.click()  # Unticking the checkbox

            except NoSuchElementException:
                return ticked_checkboxes  # Return when no more rows are found

        row += 1

def retick_checkboxes(driver, ticked_checkboxes):
    for row, col in ticked_checkboxes:
        checkbox_selector = f"#contributorform > fieldset > table > tbody > tr:nth-child({row}) > td:nth-child({col}) > input[type=checkbox]"
        checkbox = driver.find_element_by_css_selector(checkbox_selector)
        if not checkbox.is_selected():
            checkbox.click()
#To do write liberosetextractor
def liberoSetExtractor(driver):
    print("is a libero platform - extracting sets")
    #go to processing steps
    goToProcessing = "#subnav > li:nth-child(7)"
    goToProcessingBox = driver.find_element('css selector', goToProcessing)
    goToProcessingBox.click()
    sleep(0.5)
    print("got to processing for libero")
    editTestProcessingSteps = "#content > ul:nth-child(6) > li:nth-child(1) > a"
    editTestProcessingStepsBox = driver.find_element('css selector', editTestProcessingSteps)
    editTestProcessingStepsBox.click()
    sleep(0.5)
    print("got to processing steps for libero")
    #click on processing steps button
    # Click the element
    click_element_selector = "#ProcessingStepsForm > table > tbody > tr:nth-child(4) > td:nth-child(8) > ul > li:nth-child(1) > a"
    driver.find_element(By.CSS_SELECTOR, click_element_selector).click()

    # Extract the value from the first input field and save as 'liberoFieldName'
    field_name_selector = "#processingstepform > dl > dd:nth-child(16) > table > tbody > tr.clone > td:nth-child(1) > input"
    liberoFieldName = driver.find_element(By.CSS_SELECTOR, field_name_selector).get_attribute("value")

    # Extract the value from the second input field and save as 'liberoRequiredValue'
    required_value_selector = "#processingstepform > dl > dd:nth-child(16) > table > tbody > tr.clone > td:nth-child(2) > input"
    liberoRequiredValue = driver.find_element(By.CSS_SELECTOR, required_value_selector).get_attribute("value")
    return driver, liberoFieldName, liberoRequiredValue

def liberoStepInsert(driver, liberoFieldName, liberoRequiredValue):
    print("is a libero platform - inserting sets exclusions")
    #go to processing steps
    goToProcessing = "#subnav > li:nth-child(6)"
    goToProcessingBox = driver.find_element('css selector', goToProcessing)
    goToProcessingBox.click()
    sleep(0.5)
    print("got to processing for libero")
    editTestProcessingSteps = "#content > ul:nth-child(6) > li:nth-child(1) > a"
    editTestProcessingStepsBox = driver.find_element('css selector', editTestProcessingSteps)
    editTestProcessingStepsBox.click()
    sleep(0.5)
    print("got to edit test processing steps for libero")
    #click on processing steps button
    # Click the element
    click_element_selector = "#ProcessingStepsForm > table > tbody > tr:nth-child(4) > td:nth-child(8) > ul > li:nth-child(1) > a"
    driver.find_element(By.CSS_SELECTOR, click_element_selector).click()

    # Extract the value from the first input field and save as 'liberoFieldName'
    field_name_selector = "#processingstepform > dl > dd:nth-child(16) > table > tbody > tr.clone > td:nth-child(1) > input"
    driver.find_element(By.CSS_SELECTOR, field_name_selector).send_keys(liberoFieldName)

    # Extract the value from the second input field and save as 'liberoRequiredValue'
    required_value_selector = "#processingstepform > dl > dd:nth-child(16) > table > tbody > tr.clone > td:nth-child(2) > input"
    driver.find_element(By.CSS_SELECTOR, required_value_selector).send_keys(liberoRequiredValue)

    main_submit_selector = "#mainsubmit"
    driver.find_element(By.CSS_SELECTOR, main_submit_selector).click()

    # Click the element using its specific CSS path
    processing_step_selector = "#ProcessingStepsForm > ul:nth-child(5) > li:nth-child(2) > input"
    driver.find_element(By.CSS_SELECTOR, processing_step_selector).click()

    return driver


def contributorVariables(driver, contributorNamevalue):
    
    editContributor = driver.find_element(By.CSS_SELECTOR, "#content > ul > li:nth-child(1) > a")
    editContributorvalue = editContributor.click()
    sleep(0.5)
    print("got passed edit")

    contributorNUC = extract_contributor_NUC(contributorNamevalue)
    print("got passed NUC extraction")
    print(contributorNUC)

    description = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(4) > input[type=text]")
    descriptionvalue = description.get_attribute("value")
    print("got passed description")
    print(descriptionvalue)
    
    platform = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(10) > input[type=text]")
    platformValue = platform.get_attribute("value")  # Retrieve the current value of the element
    print("got passed platform")

# Convert the platformValue to lowercase for case-insensitive comparison
    platformValueLower = platformValue.lower()

# Check if the lowercase platformValue is one of the specified strings
    if platformValueLower in ("symphony", "sirsidynix"):
        platformValue = "SirsiDynix"
    if platformValueLower in ("alma", esploro)
        platformValue = "Alma"
    print("got passed platform logic")
    print("checking to see if this prints")
    print(platformValue)
    print("platform value should have printed")
    orgID = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(12) > input[type=text]")
    orgIDvalue = orgID.get_attribute("value")
    print("got passed orgID")
    print(orgIDvalue)
    print("about to turnoff and copy notification settings")
    ticked_checkboxes = check_and_untick_checkboxes(driver)

    
    # Locate the <select> element
    workEffort_dropdown = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(14) > select")
    print("found it")
    # Create a Select object
    select_element = Select(workEffort_dropdown)
    print("created select object")
    # Retrieve the currently selected option
    selected_option = select_element.first_selected_option
    workEffortvalue = selected_option.get_attribute("value")
    print("Selected work effort value:", workEffortvalue)
    print(workEffortvalue)
    # need to confirm all of the selectors are right - mightve screwed it
    #  = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(10) > input[type=text]")
    # contributorNamevalue = contributorName.get_attribute("value")

    return driver, contributorNUC, descriptionvalue, platformValue, orgIDvalue, workEffortvalue



def extract_contributor_NUC(contributorNamevalue):
    # Regular expression to find all characters up to the first space
    match = re.search(r'(\S+)', contributorNamevalue)
    if match:
        # Extract the value up to the first space
        contributorNUCvalue = match.group(1)
    else:
        # Handle cases where no match is found
        print("I could not figure out what your NUC value was")

    return contributorNUCvalue


def contributorDetailsVariables(driver):
    base_selector = "#contributorform > fieldset > table > tbody > tr:nth-child({}) > td:nth-child({}) > input"
    contributors = []
    index = 4

    while True:
        try:
            print("got to name_select")
            name_selector = base_selector.format(index, 1)
            job_title_selector = base_selector.format(index, 2)
            email_selector = base_selector.format(index, 3)
            type_selector = base_selector.format(index, 7)

            name_field = driver.find_element(By.CSS_SELECTOR, name_selector)
            job_title_field = driver.find_element(By.CSS_SELECTOR, job_title_selector)
            email_field = driver.find_element(By.CSS_SELECTOR, email_selector)
            type_field = driver.find_element(By.CSS_SELECTOR, type_selector)
            print("details found")
            contributors.append({
                'name': name_field.get_attribute("value"),
                'job_title': job_title_field.get_attribute("value"),
                'email': email_field.get_attribute("value"),
                'type': type_field.get_attribute("value")
            })
            print("details appended")
            index += 1
        except Exception as e:
            # No more contributors
            print("No more contributors")
            break

    return driver, contributors


def connectionSettingsVariables(driver):
    print("got to connectionsettings variables")
    viewConnectionSettings = driver.find_element(By.CSS_SELECTOR, "#subnav > li:nth-child(3) > a")
    viewConnectionSettingsBox = viewConnectionSettings.click()
    sleep(0.5)
    print("got to connection settings ul > li > a")
    editConnectionSettingsAgain = driver.find_element(By.CSS_SELECTOR, "#content > ul > li > a")
    editConnectionSettingsAgainBox = editConnectionSettingsAgain.click()
    sleep(0.5)
    print("first connection edit?")
    step2ConnectionSettings = driver.find_element(By.CSS_SELECTOR, "#step1 > ul > li:nth-child(2) > a")
    step2ConnectionSettingsBox = step2ConnectionSettings.click()
    print("second connection edit?")
    
    urlTaker = driver.find_element(By.CSS_SELECTOR, "#settingsform > fieldset > dl > dd:nth-child(4) > input")
    urlTakervalue = urlTaker.get_attribute("value")
    print("got passed urlTaker")
    print(urlTakervalue)
    #settingsform > fieldset > dl > dd:nth-child(4) > input
    step3ConnectionSettings = driver.find_element(By.CSS_SELECTOR, "#settingsform > ul > li:nth-child(3) > a")
    step3ConnectionSettingsBox = step3ConnectionSettings.click()

    setTaker_dropdown = driver.find_element(By.CSS_SELECTOR, "#settingsform > fieldset > dl > dd:nth-child(6) > select")

    # Create a Select object
    select_element = Select(setTaker_dropdown)

    # Get the currently selected option
    selected_option = select_element.first_selected_option
    setTakervalue = selected_option.get_attribute("value")

    print("Selected set taker value:", setTakervalue)

    return driver, urlTakervalue, setTakervalue



# def checkCustomOrStandardProcessingStepsAndCopyLiberoStep(driver, Platform): #unfinished - do it later
    #subnav > li:nth-child(7) > a 
    #content > ul:nth-child(6) > li:nth-child(1) > a 

    # Custom if it has effortVariable == custom or customSteps or has notes (uses create 850 held only, or any other unique held stylesheet, uses any other unexpected steps - do a list of acceptable step names <-- will need to go into each one.)
    
    # return driver, liberoStep, customBoolean



def logsDownloadOldSheetForComparison(driver, contributorNamevalue):

    #download from logs
    openLogs2 = "#subnav > li:nth-child(8) > a"
    openLogs2box = driver.find_element('css selector', openLogs2)
    openLogs2box.click()
    sleep(0.5)
    print("got to downloads")
    openMostRecentHarvest = "#content > table > tbody > tr:nth-child(2) > td:nth-child(1) > a"
    openMostRecentHarvestbox = driver.find_element('css selector', openMostRecentHarvest)
    openMostRecentHarvestbox.click()
    sleep(0.5)
    print("got to specific harvest")
    sleep(3)
    downloadAll2 = "#content > dl:nth-child(3) > dd:nth-child(9) > ul > li:nth-child(3) > a"
    downloadAll2Box = driver.find_element('css selector', downloadAll2)  # Find the element using the CSS selector
    actions = ActionChains(driver)
    actions.key_down(Keys.ALT).click(downloadAll2Box).key_up(Keys.ALT).perform()  # Perform Alt+Click on the element
    print("downloaded logs")
    sleep(0.5)
    base_path = r"C:\Users\lknoke\Downloads\NLA\HarvesterANBDtoANBS"
    destination_path = os.path.join(base_path, contributorNamevalue)
    move_most_recent_download(r"C:\Users\lknoke\Downloads", destination_path)
    
    return driver

def move_most_recent_download(source_directory, destination_directory):
    # Get the list of files in the downloads directory
    files = os.listdir(source_directory)
    # Create full paths to the files
    full_paths = [os.path.join(source_directory, file) for file in files]
    
    # Filter out directories, only keep files
    files_only = [file for file in full_paths if os.path.isfile(file)]
    
    # Find the most recent file
    most_recent_file = max(files_only, key=os.path.getctime)
    
    # Construct the destination path
    destination_file_path = os.path.join(destination_directory, os.path.basename(most_recent_file))
    
    # Move the most recent file to the destination directory
    shutil.move(most_recent_file, destination_file_path)
    print(f"Moved {most_recent_file} to {destination_directory}")


def create_new_contributor(driver, liberoSets, contributorNamevalue, contributorNUCvalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue, urlTakervalue, setTakervalue, contributors):

    # need to break out the data variable array for the individual variable names to call and insert them where relevant for the following functions
    url = "https://ourweb.nla.gov.au/HarvesterClient/ListCollections.htm"
    driver.get(url)
    print("going home page")
    driver = createNewContributorBegin(driver)
    print("created new contributor")
    driver = inputContributorDetails(driver, contributorNamevalue, orgIDvalue, workEffortvalue, platformValue, descriptionvalue)
    print("inputted new contributor details")
    driver = addContributorContactDetails(driver, contributors)
    print("added contact details")
    driver = inputConnectionDetails(driver, urlTakervalue, setTakervalue)
    print("connection details done")
    driver = inputDataStoreSettings(driver, contributorNUCvalue)
    print("data store done")
    driver = editProcessingSteps(driver, liberoSets, contributorNUCvalue)
    print("processing steps eddited")
    driver = runTestHarvest(driver)
    print("test harvest run")
    driver = downloadLogs(driver, contributorNamevalue)
    print("logs downloaded")
    print("forgot to add in the correct folder and marcpath in the following function")
    # convert_marc_formats(contributorNamevalue, folderPath, marcPath) #these should be hardcoded for me #to do todo
    return driver

def inputDataStoreSettings(driver, contributorNUCvalue):
    
    gotoDataStore = "#subnav > li:nth-child(4) > a"
    gotoDataStoreBox = driver.find_element(By.CSS_SELECTOR, gotoDataStore)
    gotoDataStoreBox.click()
    print("this ul li a is datastore")
    editDataStore = "#content > ul > li > a"
    editDataStoreBox = driver.find_element(By.CSS_SELECTOR, editDataStore)
    editDataStoreBox.click()

    editNuc = "#settingsform > fieldset > dl > dd:nth-child(2) > input"
    editNucBox = driver.find_element(By.CSS_SELECTOR, editNuc)
    editNucBox.send_keys(contributorNUCvalue)

    saveDataStore = "#settingsform > ul > li:nth-child(2) > a"
    saveDataStoreBox = driver.find_element(By.CSS_SELECTOR, saveDataStore)
    saveDataStoreBox.click()

    return driver

def createNewContributorBegin(driver):
    print("selecting ANBS Path")

    anbs_path = "#content > table > tbody > tr:nth-child(14) > td:nth-child(1) > a"
    anbs_box = driver.find_element('css selector', anbs_path)
    anbs_box.click()
    sleep(0.5)
    
    anbs_addnew = "#content > ul > li > a"
    anbs_addnew_box = driver.find_element('css selector', anbs_addnew)
    anbs_addnew_box.click()
    sleep(0.5)

    return driver

def inputContributorDetails(driver, contributorNamevalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue):
    # Start with the first input field
    name_insert = "#contributorform > fieldset > dl > dd:nth-child(2) > input[type=text]"
    name_insertBox = driver.find_element(By.CSS_SELECTOR, name_insert)
    name_insertBox.click()  # Focus on the name insert box

    # Now send the keys in sequence, using TAB to navigate between fields
    name_insertBox.send_keys(contributorNamevalue)
    name_insertBox.send_keys(Keys.TAB)
    name_insertBox.send_keys(descriptionvalue)
    name_insertBox.send_keys(Keys.TAB)
    name_insertBox.send_keys(platformValue)
    name_insertBox.send_keys(Keys.TAB)
    name_insertBox.send_keys(orgIDvalue)
    name_insertBox.send_keys(Keys.TAB)
    print("added orgid")
    # Locate the <select> element for workEffort
    workEffort_dropdown = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(14) > select")

# Create a Select object for the workEffort dropdown
    select_workEffort = Select(workEffort_dropdown)
# Assuming workEffortvalue holds the value of the option you want to select
# Select the option by its value in the workEffort dropdown
    select_workEffort.select_by_value(workEffortvalue)
    print("selected workeffort")


    print(f"workEffort option with value '{workEffortvalue}' selected")
    return driver



def addContributorContactDetails(driver, contributors):
    for i, contributor in enumerate(contributors, start=4):
        # Construct the selector for each field based on the index
        name_selector = f"#contributorform > fieldset > table > tbody > tr:nth-child({i}) > td:nth-child(1) > input"
        job_title_selector = f"#contributorform > fieldset > table > tbody > tr:nth-child({i}) > td:nth-child(2) > input"
        email_selector = f"#contributorform > fieldset > table > tbody > tr:nth-child({i}) > td:nth-child(3) > input"
        print("forgot to add type of contributor")
        # Find and populate the name field
        name_field = driver.find_element(By.CSS_SELECTOR, name_selector)
        name_field.clear()
        name_field.send_keys(contributor['name'])

        # Find and populate the job title field
        job_title_field = driver.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title_field.clear()
        job_title_field.send_keys(contributor['job_title'])

        # Find and populate the email field
        email_field = driver.find_element(By.CSS_SELECTOR, email_selector)
        email_field.clear()
        email_field.send_keys(contributor['email'])

        # Logic to handle T or B typing based on box
        # You need to add this logic based on your specific requirements

        # Logic for handling if there are more contributors (like a "Add More" button)
        # This part of the code needs to be implemented according to the specific functionality of your webpage

    # Click the submit/connection button after adding all contributors
    setConnectionPath = "#mainsubmit"
    setConnectionBox = driver.find_element(By.CSS_SELECTOR, setConnectionPath)
    setConnectionBox.click()
    sleep(0.5)

    return driver


def inputConnectionDetails(driver, urlTakervalue, setTakervalue, platformValue):
    # Input URL
    urlPath = "#settingsform > fieldset > dl > dd:nth-child(6) > input"
    urlPathBox = driver.find_element(By.CSS_SELECTOR, urlPath)
    urlPathBox.send_keys(urlTakervalue)

    # Save Connection Settings
    saveConnectionSettings = "#settingsform > ul > li:nth-child(3) > a"
    saveConnectionSettingsBox = driver.find_element(By.CSS_SELECTOR, saveConnectionSettings)
    saveConnectionSettingsBox.click()
    sleep(0.5)

    # Input SET and navigate to format selection
    setInsert = "#settingsform > fieldset > dl > dd:nth-child(8) > input[type=text]"
    setInsertBox = driver.find_element(By.CSS_SELECTOR, setInsert)
    # Locate the <select> element
    setTaker_dropdown = driver.find_element(By.CSS_SELECTOR, "#settingsform > fieldset > dl > dd:nth-child(6) > select")

    # Create a Select object
    select_element = Select(setTaker_dropdown)

    # Assuming setTakervalue holds the value of the option you want to select
    # Select the option by its value
    select_element.select_by_value(setTakervalue)

    print(f"Option with value '{setTakervalue}' selected")
    setInsertBox.send_keys(Keys.TAB)

    # Clear the existing format value and input "marc21"
    for _ in range(6):  # Assuming 6 backspaces are sufficient to clear the field
        setInsertBox.send_keys(Keys.BACKSPACE)
    setInsertBox.send_keys("marc21")

    # Navigate to the next field and input the value "500"
    setInsertBox.send_keys(Keys.TAB)
    setInsertBox.send_keys("500")
    setInsertBox.send_keys(Keys.TAB)

    # Input Platform Value
    setInsertBox.send_keys(platformValue)

    # Submit the form
    saveContributor = "#mainsubmit"
    saveContributorBox = driver.find_element(By.CSS_SELECTOR, saveContributor)
    saveContributorBox.click()
    sleep(0.5)

    return driver






def initialize_csv(csv_filename='output.csv'):
    # Open the file in write mode to create or clear the file
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write a header
        writer.writerow(['Contributor Name'])

def write_to_csv(contributorNamevalue, workEffortvalue, csv_filename='output.csv'):
    # Check if workEffortvalue is 'custom'
    if workEffortvalue == 'custom':
        # Open the file in append mode
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([contributorNamevalue])

        



    #MAY NEED TO BE REALLY CAREFUL HERE AS NUMBER OF PROCESSING STEPS WILL CHANGE DEPENDING ON PROCESSING PROFILE


def editProcessingSteps(driver, platformVariable, liberoSets, contributorNUCvalue):
    goToProcessing = "#subnav > li:nth-child(7)"          
    goToProcessingBox = driver.find_element('css selector', goToProcessing)     
    goToProcessingBox.click()
    #content > ul:nth-child(6) > li:nth-child(1) > a
    print("got to processing")
    
    editTestProcessingSteps = "#content > ul:nth-child(6) > li:nth-child(1) > a"
    editTestProcessingStepsBox = driver.find_element('css selector', editTestProcessingSteps)
    editTestProcessingStepsBox.click()


    if platformVariable.lower() == "libero":
        print("got to libero")
        editLiberoProcessingSteps(driver, liberoSets, contributorNUCvalue)

    # edit test steps - I have not changed this yet - need to look at it later - def wrong
    driver = clickProcessingStepButton(driver, platformVariable)
    sleep(0.5)
    
    print("processing step opened")
    
    editNucStep = "#ProcessingStepsForm > table > tbody > tr:nth-child(11) > td:nth-child(8) > ul > li:nth-child(1) > a"
    editNucStepBox = driver.find_element('css selector', editNucStep)
    editNucStepBox.click()
    sleep(0.5)
    
    insertNUCText = "#processingstepform > dl > dd:nth-child(16) > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr.clone > td:nth-child(2) > input"
    insertNUCTextbox = driver.find_element('css selector', insertNUCText)
    insertNUCTextbox.send_keys(contributorNUCvalue)
    sleep(0.5)
    print("added NUC")
   
    replaceCHANGE = "#processingstepform > dl > dd:nth-child(12) > input[type=text]"
    replaceCHANGEbox = driver.find_element('css selector', replaceCHANGE)
    replaceCHANGEbox.click()
    sleep(0.5)
    print("forgot to add NUC change replace code")
    saveNuc = "#mainsubmit"
    saveNucbox = driver.find_element('css selector', saveNuc)
    saveNucbox.click()
    sleep(0.5)
    
    
    saveSteps = "#ProcessingStepsForm > ul:nth-child(5) > li:nth-child(2) > input"
    saveStepsbox = driver.find_element('css selector', saveSteps)
    saveStepsbox.click()
    sleep(0.5)
    print("finished processing steps")

    return driver


def clickProcessingStepButton(driver, platformVariable):
    # Determine the correct row index based on platformVariable
    row_index = 9 if platformVariable.lower() == "libero" else 8

    # Construct the selector for the button
    button_selector = f"#ProcessingStepsForm > table > tbody > tr:nth-child({row_index}) > td:nth-child(8) > ul > li:nth-child(1) > a"

    # Find the button and click it
    button = driver.find_element(By.CSS_SELECTOR, button_selector)
    button.click()
    sleep(0.5)

    return driver


def runTestHarvest(driver):
    
    
    performTestHarvest = "#subnav > li:nth-child(6) > a"
    performTestHarvestbox = driver.find_element('css selector', performTestHarvest)
    performTestHarvestbox.click()
    sleep(0.5)
    
    print("got to test")
    fiftyRecords = "#manual > dd:nth-child(6) > dl > dd:nth-child(3) > input:nth-child(3)"
    fiftyRecordsbox = driver.find_element('css selector', fiftyRecords)
    fiftyRecordsbox.click()
    sleep(0.5)

    print("selected from earliest")
    #the below may break it as it does not exist on first harvest.
    fromTheEarliest = "#manual > dd:nth-child(6) > dl > dd:nth-child(5) > input:nth-child(6)"
    fromTheEarliestbox = driver.find_element('css selector', fromTheEarliest)
    fromTheEarliestbox.click()
    sleep(0.5)

    print("selected after 50")
    harvest = "#mainsubmit"
    harvestbox = driver.find_element('css selector', harvest)
    harvestbox.click()
    sleep(0.5)
    print("test harvest set to run")
    return driver

def downloadLogs(driver, contributorNamevalue):
    logs = "#subnav > li.on > a"
    logsbox = driver.find_element(By.CSS_SELECTOR, logs)
    logsbox.click()

    openMostRecentHarvest2 = "#content > table > tbody > tr:nth-child(2) > td:nth-child(1) > a"
    openMostRecentHarvestbox2 = driver.find_element(By.CSS_SELECTOR, openMostRecentHarvest2)
    openMostRecentHarvestbox2.click()

    create_download_folder("ANBS", contributorNamevalue)

    downloadAll = "#content > dl:nth-child(3) > dd:nth-child(9) > ul > li:nth-child(3) > a"
    downloadAllbox = driver.find_element(By.CSS_SELECTOR, downloadAll)
    downloadAllbox.click()

    return driver



def create_download_folder(db, contributorNamevalue):
    
    folder_path = os.path.join(r"C:\Users\lknoke\Downloads\NLA\HarvesterANBDtoANBS", contributorNamevalue)  # Specify the parent directory
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def output_csv(array_data, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in array_data:
            writer.writerow(row)

# Example usage for outputting a CSV
# array_data = [["Header1", "Header2"], ["Row1Data1", "Row1Data2"]]
# csv_file_path = os.path.join(download_folder, "output.csv")
# output_csv(array_data, csv_file_path)

def add_boolean_to_csv(array_data, boolean_variable, file_path):
    modified_data = []
    for row in array_data:
        new_row = row.copy()  # Copy the original row
        new_row.append("True" if boolean_variable else "False")  # Add "True" or "False"
        modified_data.append(new_row)

    output_csv(modified_data, file_path)

# Example usage
# boolean_variable = True  # Set this based on your condition
# add_boolean_to_csv(array_data, boolean_variable, csv_file_path)

def convert_marcxml_to_marc21(source_file, destination_file):
    command = f"%MARCEDIT%/cmarcedit.exe -s \"{source_file}\" -d \"{destination_file}\" -xmlmarc -utf8"
    subprocess.run(command, shell=True)

def convert_marc_to_mrk(source_file, destination_file):
    command = f"%MARCEDIT%/cmarcedit.exe -s \"{source_file}\" -d \"{destination_file}\" -break -utf8"
    subprocess.run(command, shell=True)

# # Example usage
# contributorNamevalue = "MYNUC"  # Replace with actual value
# folder_path = f"C:\\Users\\lachlan\\Downloads\\HarvesterANBDtoANBS\\ANBS {contributorNamevalue}"

# # Assuming the source file name and format
# source_marcxml_file = os.path.join(folder_path, "source_file.xml")
# intermediate_marc21_file = os.path.join(folder_path, "intermediate_file.mrc")
# final_mrk_file = os.path.join(folder_path, "final_file.mrk")

# # Convert MARCXML to MARC21
# convert_marcxml_to_marc21(source_marcxml_file, intermediate_marc21_file)

# # Convert MARC21 to MRK
# convert_marc_to_mrk(intermediate_marc21_file, final_mrk_file)


# #more exammple apparently
# marcedit_path = os.getenv('MARCEDIT')

# Use `marcedit_path` in your subprocess calls
# Example:
# subprocess.run(f"{marcedit_path} -s input_file -d output_file -task ...", shell=True)


# if enviornment path is locked 
# downloadLogsmarcedit_path = "C:\\path\\to\\MarcEdit\\cmarcedit.exe"
# # Use `marcedit_path` in your script



def convert_marc_formats(contributor_name, folder_path, marcedit_path):
    # Construct the file paths
    source_marcxml_file = os.path.join(folder_path, f"{contributor_name}_source_file.xml")
    intermediate_marc21_file = os.path.join(folder_path, f"{contributor_name}_intermediate_file.mrc")
    final_mrk_file = os.path.join(folder_path, f"{contributor_name}_final_file.mrk")

    # Convert MARCXML to MARC21
    marcxml_to_marc21_cmd = f"{marcedit_path} -s \"{source_marcxml_file}\" -d \"{intermediate_marc21_file}\" -xmlmarc -utf8"
    subprocess.run(marcxml_to_marc21_cmd, shell=True)
    print(f"Converted MARCXML to MARC21: {intermediate_marc21_file}")

    # Convert MARC21 to MRK
    marc21_to_mrk_cmd = f"{marcedit_path} -s \"{intermediate_marc21_file}\" -d \"{final_mrk_file}\" -break -utf8"
    subprocess.run(marc21_to_mrk_cmd, shell=True)
    print(f"Converted MARC21 to MRK: {final_mrk_file}")

# Example usage
# contributorNamevalue = "MYNUC"  # Replace with actual value
# folder_path = f"C:\\Users\\lachlan\\Downloads\\HarvesterANBDtoANBS\\ANBS{contributorNamevalue}"
# marcedit_path = "C:\\path\\to\\MarcEdit\\cmarcedit.exe"  # Ensure this is the correct path to cmarcedit.exe

# convert_marc_formats(contributorNamevalue, folder_path, marcedit_path)

#to check
def notesPresenceChecker(driver):
    print("checking for presence of notes to determine if it is custom")
    presenceOfNotes = "No"

    # CSS selector for the element  
    element_selector = "#content > table > tbody > tr:nth-child(2) > td:nth-child(4) > ul > li > a"

    try:
        # Try to find the element
        driver.find_element(By.CSS_SELECTOR, element_selector)
        # If found, set presenceOfNotes to "Yes"
        presenceOfNotes = "Yes"
    except NoSuchElementException:
        # If the element is not found, NoSuchElementException is raised
        presenceOfNotes = "No"
    print("notes presence checked for")
    return driver, presenceOfNotes

#todo to check
def minimumPresenceChecker(driver):
    print("Checking for presence of minimum fields to determine if it is custom")

    # List of texts to search for in the specified column
    required_texts = [
        "Strip Namespaces",
        "Strip invalid '#' character from Leader and Control Fields",
        "Test for minimum record standard",
        "Keep only records that meet minimum record standard",
        "A MINIMUM of ONE HOLDINGS XSLT",
        "Add missing 338s",
        "Update NUC",
        "Split ISBN from other data",
        "MARC",
        "Generate SOLR query",
        "Ensure SOLR query string is not blank",
        "Evaluate results returned",
        "001",
        "Delete Duplicate 850",
        "Add MarcXML namespaces"
    ]

    # Selector for the rows in the specific column
    row_selector = "#content > table:nth-child(4) > tbody > tr"

    # Set minimumPresence to True initially
    minimumPresence = True

    try:
        # Fetch all rows in the specified column
        rows = driver.find_elements(By.CSS_SELECTOR, row_selector)
        for required_text in required_texts:
            if not any(required_text in row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text for row in rows):
                minimumPresence = False
                break
    except NoSuchElementException:
        # If rows are not found, set minimumPresence to False
        minimumPresence = False

    print(f"Minimum Presence: {minimumPresence}")
    return driver, minimumPresence

#to do todo
def compare_elements_with_standards(driver):
    # Initialize and manually assign values
    standards_array = ["Strip Namespaces", 
                       "Strip invalid '#' character from Leader and Control Fields", 
                       "CHANGE - Filter partner collections - only keep MARC_DATAFIELD is VALUE", 
                       "Test for minimum record standard",
                       "keep only records that meet minimum standard",
                       "HOLDINGS - Alma - Create 850 holding statement",
                       "HOLDINGS - Aurora/Symphony - Create 850 from 984 or add HELD",
                       "HOLDINGS - Koha - Create 850 holdings statement",
                       "HOLDINGS - Libero - Create 850 from 852",
                       "HOLDINGS - Liberty - Create 850 from 852",
                       "HOLDINGS - Spydus - Create 850 from 852",
                       "HOLDINGS - Add 850 HELD",
                       "Add missing 338 to incoming record",
                       "MARC bibliographic transformation - libraries that Catalogue",
                       "Generate SOLR query - libraries that actively catalogue",
                       "Ensure SOLR query string is not blank",
                       "Send search query string to LA Search (SOLR - prod)",
                       "Parse SOLR output",
                       "Add best matching AN parsed XML",
                       "Discard records that had a 001 added",
                       "Update NUC",
                       "Delete duplicate 850",
                       "Add MarcXML namespaces"
                       ]  # Manually assigned standard texts
    base_xpath = '//*[@id="ProcessingStepsForm"]/table/tbody'  # Manually assigned base XPath
    column_number = 6  # Manually assigned column number containing the descriptions
    
    non_matching_elements = []
    workEffort = "Standard"
    row_number = 2  # Starting from the first row you want to check

    while True:
        xpath = f"{base_xpath}/tr[{row_number}]/td[{column_number}]"
        try:
            element = driver.find_element(By.XPATH, xpath)
            element_text = element.text.strip()
            
            if element_text not in standards_array:
                non_matching_elements.append(element_text)
                workEffort = "Custom"
            
            row_number += 1  # Move to the next row
        except NoSuchElementException:
            # No more rows found, break the loop
            break
    return non_matching_elements, workEffort, driver

def customXSLT_step(driver, unusualSteps):
    # Standard array
    standard_array = [
        "strip-namespace_utf8.xsl",
        "parseANBD_SOLR.xsl",
        "Marc_Bibliographic_Transformation_Libraries_that_catalogue_1_9.xsl",
        "Generate_LA_search_string_libraries_that_catalogue v6-1.xsl",
        "Add_best_matching_AN-Pass_All_Fields_parsedXML v5.xsl",
        "Generic_Marc_Bibliographic_Transformation_8.xsl",
        "Generic_Marc_Holdings_Transformation_5.xsl",
        "Generic_Marc_Bibliographic_Transformation_8.xsl",
        "create_850_Koha.xsl",
        "create_850_held_only.xsl",
        "create_850_from_984.xsl",
        "Create_850_from_852_spydus.xsl",
        "create_850_from_852_Liberty.xsl",
        "create_850_from_852_Libero(1).xsl",
        "Construct a search string for LA SOLR_7.xsl",
        "bibliographic_minimum_record_test.xsl",
        "ALMA_create_850-1.6.xsl",
        "Add_best_matching_AN-seperate results-v3.xsl",
        "Add_338_new_records_1_2.xsl",
        "Add MARC namespaces.xsl",
        "Add_best_matching_AN-Pass_All_Fields_parsedXML v5.xsl",
        "Add_best_matching_AN-seperate results-v3.xsl",
        "Construct a search string for LA SOLR_7.xsl"
    ]

    customXSLT = "False"
    base_xpath = '//*[@id="processingstepform"]/dl/dd[8]/h4[2]/preceding-sibling::table[1]/tbody/tr'
    row_number = 1

    while True:
        try:
            # XPath to find the specific td content
            content_xpath = f"{base_xpath}[{row_number}]/td[3]"
            content_element = driver.find_element(By.XPATH, content_xpath)
            content_text = content_element.text

            print(f"Row {row_number} Content: {content_text}")

            if content_text not in standard_array:
                customXSLT = "True"
                unusualSteps.append(content_text)

            row_number += 1

        except NoSuchElementException:
            break

    return driver, customXSLT, unusualSteps

def customHarvestChecker(driver, workEffort, presenceOfNotes):
    goToProcessing = "#subnav > li:nth-child(7)"          
    goToProcessingBox = driver.find_element('css selector', goToProcessing)     
    goToProcessingBox.click()
    #content > ul:nth-child(6) > li:nth-child(1) > a
    print("got to processing")
    
    editProdProcessingSteps = "#content > ul:nth-child(3) > li:nth-child(1) > a"
    editProdProcessingStepsBox = driver.find_element('css selector', editProdProcessingSteps)
    editProdProcessingStepsBox.click()
    print("got to test steps to check if custom")

    unusualSteps, workEffortvalue, driver = compare_elements_with_standards(driver)
    driver, minimumPresence = minimumPresenceChecker(driver)
    driver, presenceOfNotes = notesPresenceChecker(driver)
    driver, customXSLT, unusualSteps = customXSLT_step(driver, unusualSteps)
    if workEffort == "Custom"|workEffort == "Not Selected"|customXSLT == "True"|presenceOfNotes == "True"|minimumPresence== "False"|unusualSteps=="True":
        workEffort = "Custom"

    #will check for minimum presence of certain fields
    #will check for fields that are not contained within a list
    #will check each of the steps more specifically to see if they are generally compliant with expectations
    #will check for the presence of certain notes
    #will check if was initially custom
        return driver, workEffortvalue, unusualSteps
