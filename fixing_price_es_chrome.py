#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Disable the logging popup
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)

#driver.minimize_window()
#driver.maximize_window()

driver.implicitly_wait(60)  # seconds

# navigate to the application home page
driver.get("http://www.cmegroup.com/trading/fixing-price.html#equities")

found = False
count = 1
wait_time = 15
max_refresh_count = 10

time.sleep(wait_time)

# The accept cookies policy button
wait = WebDriverWait(driver, 30)
element = wait.until(EC.element_to_be_clickable((By.ID, 'pardotCookieButton')))
element.click()

f = open('fpes.txt', 'w')

while (not found and count <= max_refresh_count):
       
    elem = driver.find_element_by_class_name('prodES')
   
    print(elem.text)
    f.write(elem.text + '\n')

    elem = driver.find_element_by_id('ESX_Price')
   
    print(elem.text)
    f.write(elem.text + '\n')

    if (elem.text == 'No Price Found' or elem.text == '-'):
        if (count < max_refresh_count):
            print('Waiting %d seconds to refresh (%d out of %d) ...' % (wait_time, count, max_refresh_count))

            time.sleep(wait_time)
            driver.refresh()
            time.sleep(5)
    else:
        found = True

    count = count + 1

# close the browser window
driver.quit()

f.close()

#raw_input('Press Enter to continue ...')

##END##
