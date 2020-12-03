from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

url = "https://marketplace.atlassian.com/search?category=Time%20tracking&product=jira"
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/home/saroar/workspace/exploring_time_tracking_apps/chromedriver')
driver.get(url)
loadingButton = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "css-1l4j2co")))
pages = 100

while loadingButton:
    loadingButton.click()
    time.sleep(10)
    
appCards = driver.find_elements_by_css_selector(".css-187scic-LargeHitContainer")
appNames = [appCard.find_element_by_tag_name("h3").text for appCard in appCards]
appDescriptions = [appCard.find_element_by_class_name("css-1lqn5mv-Body").text for appCard in appCards]
appCategories = [appCard.find_element_by_class_name("css-54xus6-CategoriesContainer").text for appCard in appCards]
driver.find_element_by_css_selector('.css-1l4j2co').click()

# storyTitles = [appNames.text for appName in appNames]

print(appNames)
print(appDescriptions)
print(appCategories)