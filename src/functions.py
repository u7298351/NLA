from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import re
import os
import subprocess
from time import sleep


# Example usage
max_iterations = 10  # Set this to control the number of iterations
scraper_main(max_iterations)
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


def scraper_main(max_iterations):
    download_folder = os.path.join("C:\\Users\\lachlan\\Downloads\\HarvesterANBDtoANBS", "ANBS" + contributorNamevalue)
    driver = start_chrome_with_download_path(download_folder)
    driver = process_csv_data(driver, max_iterations)
    driver.close()

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

    # Set the default download directory to `download_path`
    prefs = {"download.default_directory": download_path}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def process_csv_data(driver, max_iterations):
    with open('your_file.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if there is one

        for i, row in enumerate(csv_reader):
            if i >= max_iterations:
                break


            data = row[0]
            driver = collect_Input_GUI_And_CSVDetails(driver, data)

            driver, contributors = contributorDetailsVariables(driver)
            driver = addContributorContactDetails(driver, contributors)

            driver = create_new_contributor(driver, data)

    return driver


def collect_Input_GUI_And_CSVDetails(driver, data):
    url = "https://ourweb.nla.gov.au/HarvesterClient/ListCollections.htm"
    driver.get(url)
    sleep(0.5)

    anbd_path = "#content > table > tbody > tr:nth-child(5) > td:nth-child(1) > a"
    anbd_box = driver.find_element(By.CSS_SELECTOR, anbd_path)
    anbd_box.click()
    sleep(0.5)

    try:
        link_xpath = f"//a[contains(text(), '{data}')]"
        link = driver.find_element(By.XPATH, link_xpath)
        link.click()
        sleep(0.5)  # Wait for page to load after click
    except Exception as e:
        print(f"Error finding link for {data}: {e}")
    return driver


def copyContributorVariables(driver):
    # need to copy the variables from the contributor page
    # need to paste the variables into the new contributor page
    # Extract the value from the first textbox
    driver = contributorVariables(driver)
    driver = contributorDetailsVariables(driver)
    driver = connectionSettingsVariables(driver)
    driver = runTestHarvest(driver)
    driver = logsDownloadOldSheetForComparison(driver)


def contributorVariables(driver):
    editContributor = driver.find_element(By.CSS_SELECTOR, "#content > ul > li:nth-child(1) > a")
    editContributorvalue = editContributor.click()
    sleep(0.5)

    contributorName = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(2) > input[type=text]")
    contributorNamevalue = contributorName.get_attribute("value")
    
    contributorNUC = extract_contributor_NUC(contributorNamevalue)
    
    description = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(4) > input[type=text]")
    descriptionvalue = description.get_attribute("value")
    
    
    platform = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(10) > input[type=text]")
    platformValue = platform.get_attribute("value")  # Retrieve the current value of the element

# Convert the platformValue to lowercase for case-insensitive comparison
    platformValueLower = platformValue.lower()

# Check if the lowercase platformValue is one of the specified strings
    if platformValueLower in ("symphony", "sirsidynix", "aurora"):
        platformValue = "SirsiDynix"

    orgID = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(12) > input[type=text]")
    orgIDvalue = orgID.get_attribute("value")

    workEffort=driver.find_element("#contributorform > fieldset > dl > dd:nth-child(14) > select") #contributorform > fieldset > dl > dd:nth-child(14) > select > option:nth-child(2) I may need to use this instead
    workEffortvalue = workEffort.get_attribute("value")
    
# need to confirm all of the selectors are right - mightve screwed it
    #  = driver.find_element(By.CSS_SELECTOR, "#contributorform > fieldset > dl > dd:nth-child(10) > input[type=text]")
    # contributorNamevalue = contributorName.get_attribute("value")

    return driver

def extract_contributor_NUC(contributorNamevalue):
    # Regular expression to find characters between square brackets
    match = re.search(r'\[(.*?)\]', contributorNamevalue)
    if match:
        # Extract the value between brackets
        contributorNUCvalue = match.group(1)
    else:
        # Handle cases where no brackets are found
        contributorNUCvalue = ""  # or some default value

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

            name_field = driver.find_element(By.CSS_SELECTOR, name_selector)
            job_title_field = driver.find_element(By.CSS_SELECTOR, job_title_selector)
            email_field = driver.find_element(By.CSS_SELECTOR, email_selector)

            contributors.append({
                'name': name_field.get_attribute("value"),
                'job_title': job_title_field.get_attribute("value"),
                'email': email_field.get_attribute("value")
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


    return driver



def checkCustomOrStandardProcessingStepsAndCopyLiberoStep(driver, Platform): #unfinished - do it later
    #subnav > li:nth-child(7) > a  .click()
    #content > ul:nth-child(6) > li:nth-child(1) > a .click

    # Custom if it has effortVariable == custom or customSteps (uses create 850 held only, or any other unique held stylesheet, uses any other unexpected steps - do a list of acceptable step names <-- will need to go into each one.)
    return driver, liberoStep, customBoolean



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


def create_new_contributor(driver, data):

    # need to break out the data variable array for the individual variable names to call and insert them where relevant for the following functions

    driver = createNewContributorBegin(driver)
    driver = inputContributorDetails(driver)
    driver = addContributorContactDetails(driver)
    driver = inputConnectionDetails(driver)
    driver = inputDataStoreSettings(driver)
    driver = editProcessingSteps(driver)
    driver = runTestHarvest(driver)
    driver = downloadLogs(driver)
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


def inputContributorDetails(driver):
    name_insert = "#contributorform > fieldset > dl > dd:nth-child(2) > input[type=text]"
    drive = driver.find_element('css selector', name_insert)
    driver.send_keys(contributorNamevalue)
    driver.send_keys(Keys.TAB)
    driver.send_keys(descriptionvalue)
    driver.send_keys(Keys.TAB)
    driver.send_keys(platformValue)
    driver.send_keys(Keys.TAB)
    driver.send_keys(orgIDvalue)
    driver.send_keys(Keys.TAB)
    driver.send_keys(workEffort)
    driver.send_keys(Keys.TAB)
    driver.send_keys(Keys.TAB)
    driver.send_keys(Keys.ENTER)
    driver.send_keys(Keys.TAB)
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



def inputConnectionDetails(driver):
    urlPath = "#settingsform > fieldset > dl > dd:nth-child(6) > input"
    urlPathBox = driver.find_element('css selector', urlPath)
    urlPathBox = driver.send_keys(urlTakervalue)


    saveConnectionSettings = "#settingsform > ul > li:nth-child(3) > a"
    saveConnectionSettingsBox = driver.find_element('css selector', saveConnectionSettings)
    saveConnectionSettingsBox.click()
    sleep(0.5)



    setInsert = "#settingsform > fieldset > dl > dd:nth-child(8) > input[type=text]"
    setInsertBox = driver.find_element('css selector', setInsert)
 
    urlInsertBox = driver.send_keys(setTakervalue)
    driver.send_keys(Keys.TAB)
    driver.send_keys(Keys.BACKSPACE)
    driver.send_keys(Keys.BACKSPACE)
    driver.send_keys(Keys.BACKSPACE)
    driver.send_keys(Keys.BACKSPACE)
    driver.send_keys(Keys.BACKSPACE)
    driver.send_keys(Keys.BACKSPACE)
    driver.send_keys("marc21")
    
    # urlInsertBox = driver.send_keys("SET VARIABLE")
    # urlInsertBox = driver.send_keys("marcXML") #this needs correcting!
    driver.send_keys(Keys.TAB)
    urlInsertBox = driver.send_keys("500")
    driver.send_keys(Keys.TAB)
    #below will need logic for the SirsiDynix Platforms
    driver = driver.send_keys(platformValue)

    #mainsubmit
    saveContributor = "#mainsubmit"
    saveContributorBox = driver.find_element('css selector', saveContributor)
    saveContributorBox.click()
    sleep(0.5)

    sleep(0.5)
    return driver


def inputDataStoreSettings(driver):

    gotoDataStore = "#subnav > li:nth-child(4) > a"
    gotoDataStoreBox = driver.find_element('css selector', gotoDataStore)
    gotoDataStoreBox.click()
    sleep(0.5)


    editDataStore = "#content > ul > li > a"
    editDataStoreBox = driver.find_element('css selector', editDataStore)
    editDataStoreBox.click()
    sleep(0.5)

    #settingsform > fieldset > dl > dd:nth-child(2) > input
    editNuc = "    #settingsform > fieldset > dl > dd:nth-child(2) > input"
    editNucBox = driver.find_element('css selector', editNuc)
    editNucBox.send_keys(contributorNUCvalue)
    sleep(0.5)

    saveDataStore = "#settingsform > ul > li:nth-child(2) > a"
    saveDataStoreBox = driver.find_element('css selector', saveDataStore)
    saveDataStoreBox.click()
    sleep(0.5)




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


def downloadLogs(driver):
    logs = "#subnav > li.on > a"
    logsbox = driver.find_element('css selector', logs)
    logsbox.click()
    sleep(0.5)


    openMostRecentHarvest2 = "#content > table > tbody > tr:nth-child(2) > td:nth-child(1) > a"
    openMostRecentHarvestbox2 = driver.find_element('css selector', oxpenMostRecentHarvest2)
    openMostRecentHarvestbox2.click()
    sleep(0.5)
    create_download_folder("ANBS", contributorNamevalue)
    downloadAll = "#content > dl:nth-child(3) > dd:nth-child(9) > ul > li:nth-child(3) > a"
    downloadAllbox = driver.find_element('css selector', downloadAll)
    downloadAllbox.click()
    sleep(0.5)

    return driver


def create_download_folder(db, contributorNamevalue):
    folder_name = db + contributorNamevalue
    folder_path = os.path.join("C:\Users\lachlan\Downloads\HarvesterANBDtoANBS", folder_name)  # Specify the parent directory
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def output_csv(array_data, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in array_data:
            writer.writerow(row)

# Example usage for outputting a CSV
array_data = [["Header1", "Header2"], ["Row1Data1", "Row1Data2"]]
csv_file_path = os.path.join(download_folder, "output.csv")
output_csv(array_data, csv_file_path)

def add_boolean_to_csv(array_data, boolean_variable, file_path):
    modified_data = []
    for row in array_data:
        new_row = row.copy()  # Copy the original row
        new_row.append("True" if boolean_variable else "False")  # Add "True" or "False"
        modified_data.append(new_row)

    output_csv(modified_data, file_path)

# Example usage
boolean_variable = True  # Set this based on your condition
add_boolean_to_csv(array_data, boolean_variable, csv_file_path)

def convert_marcxml_to_marc21(source_file, destination_file):
    command = f"%MARCEDIT%/cmarcedit.exe -s \"{source_file}\" -d \"{destination_file}\" -xmlmarc -utf8"
    subprocess.run(command, shell=True)

def convert_marc_to_mrk(source_file, destination_file):
    command = f"%MARCEDIT%/cmarcedit.exe -s \"{source_file}\" -d \"{destination_file}\" -break -utf8"
    subprocess.run(command, shell=True)

# Example usage
contributorNamevalue = "MYNUC"  # Replace with actual value
folder_path = f"C:\\Users\\lachlan\\Downloads\\HarvesterANBDtoANBS\\ANBS {contributorNamevalue}"

# Assuming the source file name and format
source_marcxml_file = os.path.join(folder_path, "source_file.xml")
intermediate_marc21_file = os.path.join(folder_path, "intermediate_file.mrc")
final_mrk_file = os.path.join(folder_path, "final_file.mrk")

# Convert MARCXML to MARC21
convert_marcxml_to_marc21(source_marcxml_file, intermediate_marc21_file)

# Convert MARC21 to MRK
convert_marc_to_mrk(intermediate_marc21_file, final_mrk_file)


#more exammple apparently
marcedit_path = os.getenv('MARCEDIT')

# Use `marcedit_path` in your subprocess calls
# Example:
# subprocess.run(f"{marcedit_path} -s input_file -d output_file -task ...", shell=True)


# if enviornment path is locked 
# downloadLogsmarcedit_path = "C:\\path\\to\\MarcEdit\\cmarcedit.exe"
# # Use `marcedit_path` in your script