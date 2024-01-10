from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import tkinter as tk
import csv
import re
import os

import subprocess
from time import sleep


# Example usage
#need to add function inputs
#need to check logic for - platform sirsi
#need to check logic for - variable storing
#need to check logic for - description insertion - may not matter
#need to check logic for - notes - we can add it as we see it
#need to check logic for finding the correct test processing step
#building on prior one - need code to handle specific libero logic for each harvesting profile

#need seperate code for running put in active contributor section
#Idea - could add logic to check for unique XSLT sheets from the standards - and spit those out into another csv list to be consulted with later - would be helpful with universities
#need code to check if it is custom setup


#need marcedit file conversion
#need gui for general harvester creation
#need code to deal with contributor type dropdown - variable and insert.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
def collect_Input_GUI_And_CSVDetails(driver, contributorNamevalue):
    url = "https://ourweb.nla.gov.au/HarvesterClient/ListCollections.htm"
    driver.get(url)
    sleep(5)

    username = driver.find_element(By.CSS_SELECTOR, "#username")

    sleep(0.5)
    password = driver.find_element(By.CSS_SELECTOR, "#password")

    sleep(0.5)
    login = driver.find_element(By.CSS_SELECTOR, "#kc-login")
    login.click()
    sleep(1)

    anbd_path = "#content > table > tbody > tr:nth-child(5) > td:nth-child(1) > a"
    anbd_box = driver.find_element(By.CSS_SELECTOR, anbd_path)
    anbd_box.click()
    sleep(0.5)
    print(contributorNamevalue)
    contributorNamevalue = re.sub(r'^.*?\[', '', contributorNamevalue)
    print(contributorNamevalue)
    try:
        link_xpath = f"//a[contains(text(), '{contributorNamevalue}')]"
        print(contributorNamevalue)
        link = driver.find_element(By.XPATH, link_xpath)
        link.click()
        sleep(0.5)  # Wait for page to load after click
    except Exception as e:
        print(f"Error finding link for {contributorNamevalue}: {e}")
    print("found contributor")
    return driver

# Example callback function
def print_message(message):
    print(message)
def start_chrome_with_download_path(download_path):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    prefs = {"download.default_directory": download_path}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    sleep(5)
    return driver
def clean_contributor_name(name):
    # Remove square brackets and colons from the name
    cleaned_name = re.sub(r'[\[\]:]', '', name)
    return cleaned_name
# Test the function with the callback
def scraper_main(max_iterations, csv_file_path, update_gui_callback):
    print("got to scraper_main")
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        update_gui_callback("read file csv")
         # Skip the header row if there is one

        for i, row in enumerate(csv_reader):
            if i >= max_iterations:
                break

            # Assuming the contributorNamevalue is in a specific column, e.g., first column
            contributorNamevalue = row[0]  # Adjust the index as per your CSV structure
            update_gui_callback("got to contributor extraction")

            update_gui_callback(f"Processing row {i+1}: {contributorNamevalue}")
            update_gui_callback("got to contributor csv processing")
            
            # Set up the download folder for each contributor
            download_folder = os.path.join("C:\\Users\\lachlan\\Downloads\\HarvesterANBDtoANBS", "ANBS" + clean_contributor_name(contributorNamevalue))
            driver = start_chrome_with_download_path(download_folder)
            update_gui_callback("Chrome started with download path set.")
            sleep(5)
            # Rest of the processing logic
            driver = collect_Input_GUI_And_CSVDetails(driver, contributorNamevalue)
            print("collectedInputDetails")

            sleep(5)
            driver, contributorNUCvalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue, urlTakervalue, setTakervalue, contributors = copyContributorVariables(driver, contributorNamevalue)
            print("collectedcontributorvariables")

            sleep(5)

            driver = create_new_contributor(driver, contributorNamevalue, contributorNUCvalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue, urlTakervalue, setTakervalue, contributors)
            print("createdNewContributor")
            sleep(5)
            update_gui_callback(f"Row {i+1} processed successfully.")
            sleep(5)
            # Close the driver after processing each row
            update_gui_callback("driveris about to close")
            
            driver.close()

    
    update_gui_callback("Scraping completed.")



def start_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--headless") # Enable this option when code
    # is working fine to run in headless mode (without opening browser)

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def start_chrome_with_download_path(download_path):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    prefs = {"download.default_directory": download_path}
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
            driver, contributorNamevalue, contributorNUCvalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue, urlTakervalue, setTakervalue, contributors = copyContributorVariables(driver, contributorNamevalue)
            print("collectedcontributorvariables")
            driver = create_new_contributor(driver, contributorNamevalue, contributorNUCvalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue, urlTakervalue, setTakervalue, contributors)
            print("createdNewContributor")
    return driver






def copyContributorVariables(driver, contributorNamevalue):
    # Ensure all functions are called in the correct order
    # Extract variables from the contributor page
    driver, contributorNUCvalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue = contributorVariables(driver, contributorNamevalue)
    print("copied contributor setup details")
    # Process contributor details
    driver, contributors = contributorDetailsVariables(driver)
    print("copied contributor details")
    driver, urlTakervalue, setTakervalue = connectionSettingsVariables(driver)
    print("copied contributor connection settings")

    # Run test harvest
    driver = runTestHarvest(driver)
    print("ran test harvest")

    # Download logs and old sheet for comparison
    driver = logsDownloadOldSheetForComparison(driver, contributorNamevalue)
    print("downloaded logs")

    return driver, contributorNUCvalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue, urlTakervalue, setTakervalue, contributors


def contributorVariables(driver, contributorNamevalue):
    editContributor = driver.find_element(By.CSS_SELECTOR, "#content > ul > li:nth-child(1) > a")
    editContributorvalue = editContributor.click()
    sleep(0.5)
    print("got passed edit")

    
    contributorNUC = extract_contributor_NUC(contributorNamevalue)
    print("got passed NUC extraction")
    
    description = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(4) > input[type=text]")
    descriptionvalue = description.get_attribute("value")
    print("got passed description")
    
    
    platform = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(10) > input[type=text]")
    platformValue = platform.get_attribute("value")  # Retrieve the current value of the element
    print("got passed platform")

# Convert the platformValue to lowercase for case-insensitive comparison
    platformValueLower = platformValue.lower()

# Check if the lowercase platformValue is one of the specified strings
    if platformValueLower in ("symphony", "sirsidynix", "aurora", "Symphony", "Sirsidynix", "SirsiDynix", "Aurora"):
        platformValue = "SirsiDynix"
    print("got passed platform logic")

    orgID = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(12) > input[type=text]")
    orgIDvalue = orgID.get_attribute("value")
    print("got passed orgID")

    workEffort=driver.find_element("#contributorform > fieldset > dl > dd:nth-child(14) > select") #contributorform > fieldset > dl > dd:nth-child(14) > select > option:nth-child(2) I may need to use this instead
    workEffortvalue = workEffort.get_attribute("value")
    print("got passed workEffort")
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
        contributorNUCvalue = ""

    return contributorNUCvalue


def contributorDetailsVariables(driver):
    base_selector = "#contributorform > fieldset > table > tbody > tr:nth-child({}) > td:nth-child({}) > input"
    contributors = []
    index = 4

    while True:
        try:
            name_selector = base_selector.format(index, 1)
            job_title_selector = base_selector.format(index, 2)
            email_selector = base_selector.format(index, 3)
            type_selector = base_selector.format(index, 7)

            name_field = driver.find_element(By.CSS_SELECTOR, name_selector)
            job_title_field = driver.find_element(By.CSS_SELECTOR, job_title_selector)
            email_field = driver.find_element(By.CSS_SELECTOR, email_selector)
            type_field = driver.find_element(By.CSS_SELECTOR, type_selector)
            contributors.append({
                'name': name_field.get_attribute("value"),
                'job_title': job_title_field.get_attribute("value"),
                'email': email_field.get_attribute("value"),
                'type': type_field.get_attribute("value")
            })

            index += 1
        except Exception as e:
            # No more contributors
            break

    return driver, contributors


def connectionSettingsVariables(driver):
    
    viewConnectionSettings = driver.find_element(By.CSS_SELECTOR, "#subnav > li:nth-child(3) > a")
    viewConnectionSettingsBox = viewConnectionSettings.click()
    sleep(0.5)
    
    editConnectionSettingsAgain = driver.find_element(By.CSS_SELECTOR, "#content > ul > li > a")
    editConnectionSettingsAgainBox = editConnectionSettingsAgain.click()
    sleep(0.5)

    step2ConnectionSettings = driver.find_element(By.CSS_SELECTOR, "#step1 > ul > li:nth-child(2) > a")
    step2ConnectionSettingsBox = step2ConnectionSettings.click()
    
    urlTaker = driver.find_element(By.CSS_SELECTOR, "#settingsform > fieldset > dl > dd:nth-child(4) > input")
    urlTakervalue = urlTaker.get_attribute("value")

    #settingsform > fieldset > dl > dd:nth-child(4) > input
    step3ConnectionSettings = driver.find_element(By.css_selector, "#settingsform > ul > li:nth-child(3) > a")
    step3ConnectionSettingsBox = step3ConnectionSettings.click()

    setTaker = driver.find_element(By.CSS_SELECTOR, "#settingsform > fieldset > dl > dd:nth-child(6) > select")
    setTakervalue = setTaker.get_attribute("value")


    return driver, urlTakervalue, setTakervalue



# def checkCustomOrStandardProcessingStepsAndCopyLiberoStep(driver, Platform): #unfinished - do it later
    #subnav > li:nth-child(7) > a 
    #content > ul:nth-child(6) > li:nth-child(1) > a 

    # Custom if it has effortVariable == custom or customSteps or has notes (uses create 850 held only, or any other unique held stylesheet, uses any other unexpected steps - do a list of acceptable step names <-- will need to go into each one.)
    
    # return driver, liberoStep, customBoolean



def logsDownloadOldSheetForComparison(driver):

    #download from logs
    openLogs2 = "#subnav > li:nth-child(8) > a"
    openLogs2box = driver.find_element('css selector', openLogs2)
    openLogs2box.click()
    sleep(0.5)


    openMostRecentHarvest = "#content > table > tbody > tr:nth-child(2) > td:nth-child(1) > a"
    openMostRecentHarvestbox = driver.find_element('css selector', openMostRecentHarvest)
    openMostRecentHarvestbox.click()
    sleep(0.5)
   
    create_download_folder("ANBD", contributorNamevalue)

    downloadAll2 = "#content > dl:nth-child(3) > dd:nth-child(9) > ul > li:nth-child(3) > a"
    downloadAll2Box = driver.find_element('css selector', downloadAll2)
    downloadAll2Box.click()
    sleep(0.5)

    return driver


def create_new_contributor(driver, contributorNamevalue, contributorNUCvalue, descriptionvalue, platformValue, orgIDvalue, workEffortvalue, urlTakervalue, setTakervalue, contributors):

    # need to break out the data variable array for the individual variable names to call and insert them where relevant for the following functions

    driver = createNewContributorBegin(driver)
    driver = inputContributorDetails(driver, contributorNamevalue, orgIDvalue, workEffortvalue, platformValue, descriptionvalue)
    driver = addContributorContactDetails(driver, contributors)
    driver = inputConnectionDetails(driver, urlTakervalue, setTakervalue)
    driver = inputDataStoreSettings(driver, contributorNUCvalue)
    driver = editProcessingSteps(drive, contributorNUCvaluer)
    driver = runTestHarvest(driver)
    driver = downloadLogs(driver, contributorNamevalue)
    return driver


def createNewContributorBegin(driver):

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
    name_insertBox.send_keys(workEffortvalue)
    name_insertBox.send_keys(Keys.TAB)
    name_insertBox.send_keys(Keys.TAB)  # Assuming two tabs to reach the submit or next input
    name_insertBox.send_keys(Keys.ENTER)

    return driver



def addContributorContactDetails(driver, contributors):
    for i, contributor in enumerate(contributors, start=4):
        # Construct the selector for each field based on the index
        name_selector = f"#contributorform > fieldset > table > tbody > tr:nth-child({i}) > td:nth-child(1) > input"
        job_title_selector = f"#contributorform > fieldset > table > tbody > tr:nth-child({i}) > td:nth-child(2) > input"
        email_selector = f"#contributorform > fieldset > table > tbody > tr:nth-child({i}) > td:nth-child(3) > input"

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
    setInsertBox.send_keys(setTakervalue)
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




def inputDataStoreSettings(driver, contributorNUCvalue):
    gotoDataStore = "#subnav > li:nth-child(4) > a"
    gotoDataStoreBox = driver.find_element(By.CSS_SELECTOR, gotoDataStore)
    gotoDataStoreBox.click()

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




    #MAY NEED TO BE REALLY CAREFUL HERE AS NUMBER OF PROCESSING STEPS WILL CHANGE DEPENDING ON PROCESSING PROFILE


def editProcessingSteps(driver, platformVariable, NUCVariable):
    goToProcessing = "#subnav > li:nth-child(7)"            #this looked different - might not work
    goToProcessingBox = driver.find_element('css selector', goToProcessing)     
    goToProcessingBox.click()
    

    # edit test steps - I have not changed this yet - need to look at it later - def wrong
    driver = clickProcessingStepButton(driver, platformVariable)
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

    return driver

def checkIfCustom(driver):
    return driver

def enactCustomStyleSheetNotes(driver):
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
    performTestHarvest = "#subnav > li:nth-child(5) > a"
    performTestHarvestbox = driver.find_element('css selector', performTestHarvest)
    performTestHarvestbox.click()
    sleep(0.5)
    
    
    fiftyRecords = "#manual > dd:nth-child(6) > dl > dd:nth-child(5) > input:nth-child(6)"
    fiftyRecordsbox = driver.find_element('css selector', fiftyRecords)
    fiftyRecordsbox.click()
    sleep(0.5)
    #the below may break it as it does not exist on first harvest.
    fromTheEarliest = "#manual > dd:nth-child(6) > dl > dd:nth-child(3) > input:nth-child(3)"
    fromTheEarliestbox = driver.find_element('css selector', fromTheEarliest)
    fromTheEarliestbox.click()
    sleep(0.5)

    harvest = "#mainsubmit"
    harvestbox = driver.find_element('css selector', harvest)
    harvestbox.click()
    sleep(0.5)

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
    folder_name = db + contributorNamevalue
    folder_path = os.path.join(r"C:\Users\lachlan\Downloads\HarvesterANBDtoANBS", folder_name)  # Specify the parent directory
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