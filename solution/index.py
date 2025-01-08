from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

import json
import datetime
import argparse
import logging


#### Program configurations 
# Command Line 
parser = argparse.ArgumentParser(description="Uses selenium module to save all the ticks in the records table on https://aicalliance.org/cef-universe/fund-screener/")
parser.add_argument("-sd", "--separate-data", action="store_true", help="Separate data into an array of [['Page X', [ticks]], ...]")
parser.add_argument("-l", "--logs", action="store_true", help="Show logs")
args = parser.parse_args()
separate_data = args.separate_data

# intializing logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
if not args.logs:
    # not showing error and below logs
    logging.disable(level=logging.ERROR)


#### WebDriver configurations 
# browser configurations
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')  # prevents shared memory issues
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36")
# service manages the driver; location of chromedriver
service = Service("/usr/local/bin/chromedriver")

# instance of webdriver to control Chrome
browser = webdriver.Chrome(service=service, options=options)
# website takes a while to load
browser.set_page_load_timeout(60)

# url scraping
url = "https://aicalliance.org/cef-universe/fund-screener/"
timeout = 60
wait = WebDriverWait(browser, timeout)
# for chaining basic actions (movements, clicks, ) 
actions = ActionChains(browser)


def setup_before_scraping():
    tries = 0
    while tries < 3:
        try:
            print("Requesting page")
            browser.get(url)
            print("Page loaded")
            break
        except TimeoutException as e:
            print("Page load timeout reached. Refreshing page.")
            tries+=1
    if tries == 3:
        raise Exception("Web page did not load.")
    print("Waiting on cancel button presence in dom")

    handle_popup()
    wait_for_navigation_link()


def handle_popup():
    # get rid of popup onload
    cancel = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[href='#awb-close-oc__35860']")))
    actions.scroll_to_element(cancel).move_to_element(cancel).click().perform()
    print("Waiting on navigation link presence in dom")


def wait_for_navigation_link():
    # wait until one navigation link is in the dom (if one is in then all are in)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[num-pages] .pageLink1 a")))
    print("setup_for_tickers() complete")


def get_tickers():
    print("get_tickers() called")
    data = []
    # pageLinks start at 1 (.pageLink1, .pageLink2, etc.)
    # if start value is changed make sure to click on appropriate navigation link
    # as tickers will = .pageLink1 tickers! 
    START = 1

    index = START 
    while (True):
        print(f"Page: {index}")
        print("Waiting on tickers presence in dom")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-ticker]")))
        tickers = [t.text for t in browser.find_elements(By.CSS_SELECTOR, ".tab-col-ticker > [data-ticker]")]
        if separate_data:
            data.append([f"Page {index}", tickers])
        else:
            data.extend(tickers)
        print("Tickers saved")

        index+=1

        try:
            link = browser.find_element(By.CSS_SELECTOR, f".pageLink{index} a")
            # link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pageLink" + str(index) + " a")))
            browser.execute_script("arguments[0].click()", link)
        except NoSuchElementException:
            # no more pages to scrape data from
            print(f"Element .pageLink{index} not found")
            break 

        # Clicking a link causes the #load button to change its text to "loading"
        # After fetch request is complete it returns to "SEARCH"
        # Using that to detect once new data is available. 

        print("Waiting on search request to fulfill")
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#load"), "SEARCH"))
    return data


def save_data(data):
    try:
        # write data to file
        file_name = f"{datetime.datetime.now().strftime('%Y-%m-%d_%I-%M%p')}_{'separated' if separate_data else 'singular'}.json"
        with open(file_name, "w") as file:
            file.write(json.dumps(data))
        print(f"Data saved in ---> {file_name}")
    except Exception as e:
        print(f"Failed to save data: {e}")


def main():
    try:
        setup_before_scraping()
        data = get_tickers()
        save_data(data)
    except Exception as e:
        print(f"Program crashed: {e}") 


if __name__ == "__main__":
    main()
