from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

import json
import datetime
import argparse

# service manages the driver; location of chromedriver
service = Service("/usr/local/bin/chromedriver")

options = webdriver.ChromeOptions()
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--no-sandbox')  # Necessary for running in Docker
options.add_argument('--disable-dev-shm-usage')  # Prevents shared memory issues
options.add_argument('--disable-gpu')  # Disable GPU (optional, for stability)

# instance of webdriver to control Chrome
browser = webdriver.Chrome(service=service, options=options)

url = "https://aicalliance.org/cef-universe/fund-screener/"
timeout = 20

# seconds
wait = WebDriverWait(browser, timeout)

# for chaining basic actions (movements, clicks, ) 
actions = ActionChains(browser)

# Command Line 
parser = argparse.ArgumentParser(description="Uses selenium module to save all the ticks in the records table on https://aicalliance.org/cef-universe/fund-screener/")
parser.add_argument("-sd", "--separate-data", action="store_true", help="Separate data into an array of [['Page X', [ticks]], ...]")
args = parser.parse_args()
separate_data = args.separate_data

cancelled = False 

try:
    browser.get(url)

    # get rid of popup onload
    cancel = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[href='#awb-close-oc__35860']")))
    actions.scroll_to_element(cancel).move_to_element(cancel).click().perform()

    # wait until navigation link container is in the dom
    navigation = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[num-pages]")))

    # wait until one navigation link is in the dom (if one is in then all are in)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[num-pages] .pageLink1 a")))
    links = navigation.find_elements(By.CSS_SELECTOR, "[class*=pageLink] a")

    actions.scroll_to_element(links[0]).move_to_element(links[0]).click().perform()

    data = []

    #
    # The entire table refreshes upon clicking a link 
    # The links all refresh too. 
    # 

    start = 1
    end = len(links)

    def getTickers():
        index = start
        while (True):
            print(f"Page: {index}")

            print("waiting for tickers")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-ticker]")))
            tickers = browser.find_elements(By.CSS_SELECTOR, ".tab-col-ticker > [data-ticker]")
            if separate_data:
                data.append([f"Page {index}", [t.text for t in tickers]])
            else:
                data.extend([t.text for t in tickers])
            print("Tickers saved.")

            index+=1

            if index > end:
                # no need to click link or wait for search request on last page
                break

            print("waiting for link")
            link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pageLink" + str(index) + " a")))
            browser.execute_script("arguments[0].click()", link)
            print("Link clicked")

            # Clicking a link causes the #load button to change its text to "loading"
            # After fetch request is complete it returns to "SEARCH"
            # Using that to detect once new data is available. 

            print("waiting for search request")
            wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#load"), "SEARCH"))
            print("request done")
    getTickers()
except Exception:
    print(Exception)
    cancelled = True
finally: 
    if not cancelled:
        # write data to file
        file_name = f"{datetime.datetime.now()}-ticks-data-{'separated' if separate_data else 'singular'}.json"
        with open(file_name, "w") as file:
            file.write(json.dumps(data))
        print("Wrote data to ----> ", file_name)
    browser.quit()
