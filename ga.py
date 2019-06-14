# Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

# Set the URL
url = 'https://analytics.google.com/analytics/web/?authuser=0#/'
url += 'a53572537w86300453p89534365'
url += '/admin/trackingreferral-exclusion-list/'

# Open the web browser
driver = webdriver.Chrome('./chromedriver')
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
time.sleep(2)

# Add referral exclusions

time.sleep(15)
iframe = driver.find_element_by_id("galaxyIframe")
driver.execute_script("arguments[0].contentWindow.document.querySelector('#ID-m-content-content > div._GAnf > div.ID-adminTableControlBar._GAcub > div.ID-adminTableControl._GAfJb > button').click()", iframe)
# document.querySelector('.W_DECORATE_ELEMENT._GASh._GAepb._GAmc-_GAxD-_GAmc').value = 'mollie.com'
# driver.execute_script("document.querySelector('._GAD.W_DECORATE_ELEMENT._GAId').click()")
