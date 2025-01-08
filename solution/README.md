Scrape https://aicalliance.org/cef-universe/fund-screener/ ticks in the fund table.
# Dockerfile
Build the image
```
docker build -t tick-scraper .
```
Run the image to test
```
docker run tick-scraper
```
Tag image for upload to docker hub
```
docker tag tick-scraper constanthing/tick-scraper:latest
```
Push to docker hub
```
docker push constanthing/tick-scraper:latest
```
Pull image on any machine
```
docker pull constanthing/tick-scraper:latest
```
Run image
```
docker run -it constanthing/tick-scraper:latest
```
Updating code? Make sure to publish it:
```
# update local image
docker build -t tick-scraper .
docker tag tick-scraper constanthing/tick-scraper:latest
docker push constanthing/tick-scraper:latest
```
# Requirements
## Chrome Driver
- [link](https://googlechromelabs.github.io/chrome-for-testing/)

## Make sure selenium can find driver
Easiest way, add chromedriver to path:
- Mac
	- Move chromedriver to /usr/local/bin
- Windows
- Linux  
Or, add path to chromedriver in Python code when initializing instance of WebDriver:
```
chrome = webdriver.Chrome(executable_path="/path/to/driver")
```

# Creating & Running container 
## Building on device without amd64 architecture
Run 
```
docker build --platform=linux/amd64 -t [name-of-image] .
```

## Running container
```
docker run --shm-size=2g [name-of-image]
```
> --shm-size=2g  
Reduces chances of chrome crashing.


## Install requirements (selenium) 
```
pip3 install -r requirements.txt
```

## Info
The "All" option in the **select** element does not work as it results in an endless loading state.  
Therefore, instead, the code iterates through the navigation page links (.pageLinkX) and saves the 
newly loaded ticks.
```
# end usually = len(links)
while index < end:
	# save ticks 
	# press next link to load new ticks
```

It may seem unncessary to WebDriverWait.until() in the while loop. However,  
when clicking a navigation link to get a new page of ticks the navigation list 
is removed and added to the DOM (same for table).
> You can test this by opening the console in the site:
> 1. saving the table as a local variable
> 2. click navigation link 
> 3. save table again
> 4. compare the two => false  

Thus, saving a list of the navigation links is pointless as doing
```
links[index].click()
# doesn't work because it doesn't exist (StaleElementReferenceException)
# hence, the wait() code to find the new navigational link
link = wait.until(".pageLink3")
```
