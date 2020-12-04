import re
import csv

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def get_field_text_if_exists(item, selector):
    """Extracts a field by a CSS selector if exists."""
    try:
        return item.find_element_by_css_selector(selector).text
    except NoSuchElementException:
        return ""


def get_link_if_exists(item, selector):
    """Extracts an href attribute value by a CSS selector if exists."""
    try:
        return item.find_element_by_css_selector(selector).get_attribute("href")
    except NoSuchElementException:
        return ""


chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/home/saroar/workspace/exploring_time_tracking_apps/chromedriver')
wait = WebDriverWait(driver, 10)
url = "https://marketplace.atlassian.com/search?category=Time%20tracking&product=jira"
driver.get(url)

# click more until no more results to load
while True:
    try:
        more_button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'css-1l4j2co'))).click()
    except TimeoutException:
        break

# wait for results to load
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.css-187scic-LargeHitContainer')))

# parse results
results = {}
for result in driver.find_elements_by_css_selector('.css-187scic-LargeHitContainer'):
    app_name = get_field_text_if_exists(result, '.css-r7ms9i-H3-baseHeadingsCss-baseHeadingsCss-h3Css-h3Css-NameHeader')
    app_description = get_field_text_if_exists(result, '.css-1lqn5mv-Body')
    app_categories = get_field_text_if_exists(result, '.css-1hj6rt6-CategoriesStyled')
    app_link = get_link_if_exists(result, '.css-tgmll2-linkCss-linkCss-HitLinkStyled-HitLinkStyled')
    app_id = re.search("([^/]+)(?=/[^/]+/?$)", app_link).group(0)

    results[app_id] = {"app_name": app_name, "app_description": app_description, "app_categories": app_categories, "app_link": app_link}


for key in results:
   driver.get(results[key]["app_link"])
   results[key]["app_installs"] = get_field_text_if_exists(driver, ".plugin-active-installs-total")
   results[key]["app_ratings"] = get_field_text_if_exists(driver, ".plugin-rating-summary .badge")


# write to csv
header = ["app_name", "app_description", "app_categories", "app_link", "app_installs", "app_ratings"]

with open("data.csv", "w") as f:
    w = csv.DictWriter(f, header)
    w.writeheader()
    
    for _, val in sorted(results.items()):
        w.writerow(val)


driver.quit()
