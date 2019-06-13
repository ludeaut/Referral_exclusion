# Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

# Set the URL you want to webscrape from
# url = 'https://analytics.google.com/analytics/web/?authuser=1#/a69568077w106628147p111548331/admin/trackingreferral-exclusion-list/'
url = "http://kanview.ks.gov/PayRates/PayRates_Agency.aspx"

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(30)
driver.get(url)

# import pyautogui # Do sudo pip3 install pyautogui
#
# pyautogui.hotkey('ctrl', 'space')
# pyautogui.typewrite('thomas@itsnotthatkind.org')

python_button = driver.find_element_by_id('MainContent_uxLevel1_Agencies_uxAgencyBtn_33') #FHSU
python_button.click() #click fhsu link

#Selenium hands the page source to Beautiful Soup
soup_level1=BeautifulSoup(driver.page_source, 'lxml')

datalist = [] #empty list
x = 0 #counter

for link in soup_level1.find_all('a', id=re.compile("^MainContent_uxLevel2_JobTitles_uxJobTitleBtn_")):
    ##code to execute in for loop goes here

    #Selenium visits each Job Title page
    python_button = driver.find_element_by_id('MainContent_uxLevel2_JobTitles_uxJobTitleBtn_' + str(x))
    python_button.click() #click link

    #Selenium hands of the source of the specific job page to Beautiful Soup
    soup_level2=BeautifulSoup(driver.page_source, 'lxml')

    #Beautiful Soup grabs the HTML table on the page
    table = soup_level2.find_all('table')[0]

    #Giving the HTML table to pandas to put in a dataframe object
    df = pd.read_html(str(table),header=0)

    #Store the dataframe in a list
    datalist.append(df[0])

    #Ask Selenium to click the back button
    driver.execute_script("window.history.go(-1)")

    #increment the counter variable before starting the loop over
    x += 1

#loop has completed

#end the Selenium browser session
driver.quit()

#combine all pandas dataframes in the list into one big dataframe
result = pd.concat([pd.DataFrame(datalist[i]) for i in range(len(datalist))],ignore_index=True)

#convert the pandas dataframe to JSON
json_records = result.to_json(orient='records')

#get current working directory
path = os.getcwd()

#open, write, and close the file
f = open(path + "\\fhsu_payroll_data.json","w") #FHSU
f.write(json_records)
f.close()
