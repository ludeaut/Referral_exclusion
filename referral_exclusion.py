#! python3
# referral_exclusion.py - Automatically fills the referral exclusion list.
# Link to the documentation used : https://automatetheboringstuff.com/chapter18/
# Only working for the screen of a Macbook

import webbrowser
import pyautogui # Do sudo pip3 install pyautogui
import time

pyautogui.PAUSE = 0.5

# import AppKit
# screens = [(screen.frame().size.width, screen.frame().size.height)
#     for screen in AppKit.NSScreen.screens()]
# print(screens)

# Switch the keyboard input source to dutch
# Comment if you already have dutch keyboard
pyautogui.hotkey('ctrl', 'space')

# Data
domains = []
file = open('./referral_domains.txt', 'r')
referrals = file.readlines()
for referral in referrals:
    domains.append(referral)

# Open the website
url = 'https://analytics.google.com/analytics/web/?authuser=1#/'
url += 'a40160714w69262866p71360432'
url += '/admin/trackingreferral-exclusion-list/'
webbrowser.open(url, new=1)

# Set the coordinates for buttons and fields.
addReferralExclusionButton = (440, 449)
addReferralExclusionButtonColor = (212, 74, 61)
domainField = (440, 449)
createButton = (463, 539)

# Give the user a chance to kill the script.
time.sleep(5)

# TODO : Wait until the page has loaded.

# while not pyautogui.pixelMatchesColor(addReferralExclusionButton[0], addReferralExclusionButton[1], addReferralExclusionButtonColor):
#     time.sleep(0.5)

time.sleep(12)

# im = pyautogui.screenshot()
# print(im.getpixel(addReferralExclusionButton))

# Loop among the domains
for domain in domains:

    # Click Add Referral exclusion
    pyautogui.click(addReferralExclusionButton[0], addReferralExclusionButton[1])
    time.sleep(1)
    # Click the Domain Field
    pyautogui.click(domainField[0], domainField[1])
    # Delete what could be in the Domain Field
    pyautogui.hotkey('command', 'a', 'backspace')
    # Fill out the Domain Field
    pyautogui.typewrite(domain)
    # Click Create.
    pyautogui.click(createButton[0], createButton[1])
    # Scroll up
    time.sleep(1)
    pyautogui.scroll(200)

# Switch the keyboard input source to original one
# Comment if you already had dutch keyboard
pyautogui.hotkey('ctrl', 'space')
