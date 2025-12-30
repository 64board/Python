#!/usr/bin/env python3

# Download Fixing ES Price from CME web page using Firefox.
# janeiros@mbfcc.com
# 2025.11.27, fix issues with cookie button. Created Firefox version.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import os
import time

wait_time = 10

# Disable (or at least quiet) the logging messages from geckodriver.
options = Options()
# Uncomment to run headless
# options.add_argument("-headless")

# Send geckodriver logs to null device to silence them
service = Service(log_path=os.devnull)

print('Creating Selenium Firefox web driver ...')

driver = webdriver.Firefox(options=options, service=service)

#driver.minimize_window()

screen_width = driver.execute_script("return window.screen.availWidth;")
screen_height = driver.execute_script("return window.screen.availHeight;")

browser_width = 1200
browser_height = 1000

driver.set_window_size(browser_width, browser_height)

x = screen_width - browser_width
y = 0

driver.set_window_position(x, y)

driver.implicitly_wait(wait_time)  # Seconds.

# Navigate to the specific web page.
url = 'https://www.cmegroup.com/markets/fixing-price.html#equity-indices&tab_VZ7fiwi=equity-indices'
print(f'Opening web page {url} ...')
driver.get(url)

f = open('fpes_gecko.txt', 'w')

# Cookies accept button (OneTrust)
try:
    # Wait for the button to be present / clickable
    cookies_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )

    # Use JavaScript click to bypass "could not be scrolled into view"
    driver.execute_script("arguments[0].click();", cookies_button) # type: ignore
    print("Cookies banner accepted.")
except TimeoutException:
    print("Cookies banner not found (maybe already accepted or different layout).")

# Scroll down to activate table.
body = driver.find_element(By.TAG_NAME, 'body')
body.send_keys(Keys.PAGE_DOWN)

table_row = 4

found = False
count = 1
max_refresh_count = 6

while (not found and count <= max_refresh_count):

    try:
        # Scroll down and up the page to activate table after page refresh.

        # Scroll down.
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)

        # Scroll up.
        body.send_keys(Keys.PAGE_UP)

        # Description.
        description = driver.find_element(
            By.XPATH,
            f'/html/body/main/div/div[4]/div[2]/div[3]/div/div/div/div/div[3]/div[2]/div/div/div/div/div/table/tbody/tr[{table_row}]/td[1]'
        )

        # Bracket.
        bracket = driver.find_element(
            By.XPATH,
            f'/html/body/main/div/div[4]/div[2]/div[3]/div/div/div/div/div[3]/div[2]/div/div/div/div/div/table/tbody/tr[{table_row}]/td[2]'
        )

        # Product Code.
        product_code = driver.find_element(
            By.XPATH,
            f'/html/body/main/div/div[4]/div[2]/div[3]/div/div/div/div/div[3]/div[2]/div/div/div/div/div/table/tbody/tr[{table_row}]/td[3]'
        )

        # Contract.
        contract = driver.find_element(
            By.XPATH,
            f'/html/body/main/div/div[4]/div[2]/div[3]/div/div/div/div/div[3]/div[2]/div/div/div/div/div/table/tbody/tr[{table_row}]/td[4]'
        )

        # Price.
        price = driver.find_element(
            By.XPATH,
            f'/html/body/main/div/div[4]/div[2]/div[3]/div/div/div/div/div[3]/div[2]/div/div/div/div/div/table/tbody/tr[{table_row}]/td[5]'
        )

        # Timestamp.
        timestamp = driver.find_element(
            By.XPATH,
            f'/html/body/main/div/div[4]/div[2]/div[3]/div/div/div/div/div[3]/div[2]/div/div/div/div/div/table/tbody/tr[{table_row}]/td[6]'
        )

    except NoSuchElementException as e:
        print(f'No such element found: {e.msg}')

    else:
        if price.text != 'No Price Found' and price.text != '-':
            found = True
            line = f'{description.text}|{bracket.text}|{product_code.text}|{contract.text}|{price.text}|{timestamp.text}'
            print(line)
            f.write(line + '\n')
        else:
            print('No Price Found!')

    finally:
        if (not found and count < max_refresh_count):
            print('Waiting %d seconds to refresh (%d out of %d) ...' % (wait_time, count, max_refresh_count))
            time.sleep(wait_time)
            driver.refresh()

    count += 1

# Close the browser window.
print('Closing Selenium Firefox web driver ...')
driver.quit()

# Save file.
f.close()

##END##
