# Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Data
file = open('./referral_domains.txt', 'r')
referrals = file.readlines()


# Set the first URL
url = 'https://analytics.google.com/analytics/web/?authuser=0#/'
url += 'a47863448w79236753p81943376' # Part to change for each site
url += '/admin/trackingreferral-exclusion-list/'

# Open headless Chrome browser
options = Options()
options.headless = False
driver = webdriver.Chrome('./chromedriver', chrome_options=options)
driver.implicitly_wait(30)
driver.get(url)

# Get login credentials
with open("login.json", 'r') as f:
	login = json.load(f)

# Login with your Google Analytics account
driver.execute_script("document.querySelector('.whsOnd.zHQkBf').value = arguments[0]", login['email'])
driver.execute_script("document.getElementById('identifierNext').click()")
time.sleep(2)

driver.execute_script("document.querySelector('.whsOnd.zHQkBf').value = arguments[0]", login['password'])
driver.execute_script("document.getElementById('passwordNext').click()")

# # Set the second url
# part = driver.current_url.split("/")[-1]
# url = 'https://analytics.google.com/analytics/web/?authuser=0#/'
# url += part
# url += '/admin/trackingreferral-exclusion-list/'
#
# # Open the second url
# driver.get(url)

# Add referral exclusions

try:
    element = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "galaxyIframe"))
    )
finally:
    driver.switch_to_frame("galaxyIframe")
    for referral in referrals:
        if len(driver.find_elements_by_tag_name('button')) != 2:
            driver.execute_script("document.querySelector('#ID-m-content-content > div._GAnf > div.ID-adminTableControlBar._GAcub > div.ID-adminTableControl._GAfJb > button').click()")
            time.sleep(3)
        # print(referral)
        driver.execute_script("document.querySelector('#ID-m-content-content > div > form > div._GAIf > div._GAr0b > input').value = arguments[0]", referral)
        driver.execute_script("document.querySelector('#ID-m-content-content > div > form > div._GApi > button._GAD.W_DECORATE_ELEMENT._GAId').click()")
        time.sleep(2)

driver.switch_to_default_content()
driver.quit()
