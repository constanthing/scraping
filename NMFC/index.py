from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import json
from re import sub, split
from datetime import datetime

# path to binary
service = Service("/usr/local/bin/chromedriver")
# chrome options 
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36")
options.page_load_strategy = "eager" 
options.timeouts = { "pageLoad": 60000 }
browser = webdriver.Chrome(service=service, options=options)
# wait
timeout = 60 # wait a minute before throwing TimeoutException 
wait = WebDriverWait(browser, timeout)
# action chains
actions = ActionChains(browser)

def load_page():
    URL = "https://finance.yahoo.com/quote/NMFC/"
    for i in range(3):
        try:
            print("waiting on page request")
            browser.get(URL)
            print("page loaded")
            return
        except TimeoutException:
            # after 60 seconds if page does not load TimeoutException is thrown
            print("Page load timeout reached... reloading page")
    raise TimeoutException("Failed to load page...")

# cleans label e.g. "Market Cap (intraday)" -> market_cap 
def clean_label(label):
    clean_label = split(r"\(", label.lower(), maxsplit=1)[0]
    clean_label = sub(r"[ -]", "_", clean_label)
    return sub(r"[.']", "", clean_label).strip("_")

def get_data():
    quoteStatistics = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='quote-statistics']")))
    # quoteStatistics is a div containing the data 
    # data is stored in a unordered list 
    # list items have 2 type of spans in them -> span:label & span:value
    # 2 types of list-items depending on their span:value -> li:number_only & li:mixed
    # li:number_only has a <fin-streamer/> element in the span:value
    # li:mixed has no child elements in span:value ONLY text
    lis = quoteStatistics.find_elements(By.CSS_SELECTOR, "li")
    data = {}
    for li in lis:
        label = li.find_element(By.CSS_SELECTOR, ".label").text
        valueElement = li.find_element(By.CSS_SELECTOR, ".value")
        value = None
        try:
            # li is :number_only
            value = valueElement.find_element(By.CSS_SELECTOR, "fin-streamer").text
        except NoSuchElementException:
            # li is :mixed
            value = valueElement.text
        print(f"{label} - {value}")
        data[clean_label(label)] = value  
        # data.append({"label": label, "value": value})
    return data

def store_data(data):
    try:
        file_name = f"{datetime.now().strftime('%Y-%m-%d_%I-%M%p')}.json"
        with open(file_name, "w") as file:
            file.write(json.dumps(data))
        print(f"Data saved at -> {file_name}")
    except Exception as e:
        print("Failed to save data...")

def main():
    try:
        load_page()
        data = get_data()
        store_data(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        browser.quit()

if __name__ == "__main__":
    main()