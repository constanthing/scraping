from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException


import json
from datetime import datetime

# path to binary
service = Service("/usr/local/bin/chromedriver")
# chrome options 
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')  # prevents shared memory issues
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36")
# normal waits entire page to load
# eager waits for dom to load (resources like images/stylesheets are ignored)
options.page_load_strategy = "eager" 
options.timeouts = { "pageLoad": 60000 }
browser = webdriver.Chrome(service=service, options=options)
# wait
timeout = 60 # wait a minute before throwing TimeoutException 
wait = WebDriverWait(browser, timeout)
# action chains
actions = ActionChains(browser)

def load_page():
    print("waiting on page request")
    URL = "https://finance.yahoo.com/quote/NMFC/"
    browser.get(URL)
    print("page loaded")

def get_data():
    quoteStatistics = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='quote-statistics']")))
    # quoteStatistics is a div containing the data 
    # data is stored a unordered list 
    # in the list items there are 2 type of spans -> span:label & span:value
    # 2 types of list-items depending on their span:value -> li:number_only & li:mixed
    # li:number_only has a <fin-streamer/> element in the span:value
    # li:mixed has no child elements in span:value ONLY text
    lis = quoteStatistics.find_elements(By.CSS_SELECTOR, "li")
    data = []
    for li in lis:
        label = li.find_element(By.CSS_SELECTOR, ".label").text
        value = li.find_element(By.CSS_SELECTOR, ".value")
        # determine whether value is :number or :mixed
        tvalue = None
        try:
            tvalue = value.find_element(By.CSS_SELECTOR, "fin-streamer").text
        except NoSuchElementException:
            print("li not :number_only... storing :mixed value")
            tvalue = value.text
        print(f"{label} - {tvalue}")

        data.append({"label": label, "value": tvalue})
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