import csv
import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import log

URL = "https://marketplace.atlassian.com/search?category=Time%20tracking&product=jira"


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


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
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='./chromedriver')
wait = WebDriverWait(driver, 5)
driver.get(URL)

# click "More Results" till all results are loaded
while True:
    try:
        more_button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'css-1l4j2co'))).click()
        print("Loading more results. . .")
    except TimeoutException:
        print("All results are loaded.")
        break

# wait for results to load
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.css-187scic-LargeHitContainer')))

# a dict to hold the data in memory
results = {}

# creating a csv file with the header
header = ["name", "description", "categories", "vendor_name", "total_installs", "total_reviews", "has_free_trial", "is_paid", "is_free", "support_status", "is_jira_service", "link", "pricing_cloud_1", "pricing_cloud_2",
"pricing_server_1", "pricing_server_2", "pricing_server_3", "pricing_server_4", "pricing_server_5"]

with open("data.csv", "w") as f:
    w = csv.DictWriter(f, header)
    w.writeheader()

print("Reading data from the list page.")
printProgressBar(0, len(driver.find_elements_by_css_selector('.css-187scic-LargeHitContainer')), prefix = 'Progress:', suffix = 'Complete', length = 50)
# get data from the list page (given URL) and add to the dictionary
for i, result in enumerate(driver.find_elements_by_css_selector('.css-187scic-LargeHitContainer')):
    name = get_field_text_if_exists(result, '.css-r7ms9i-H3-baseHeadingsCss-baseHeadingsCss-h3Css-h3Css-NameHeader')
    description = get_field_text_if_exists(result, '.css-1lqn5mv-Body')
    categories = get_field_text_if_exists(result, '.css-1hj6rt6-CategoriesStyled')
    link = get_link_if_exists(result, '.css-tgmll2-linkCss-linkCss-HitLinkStyled-HitLinkStyled')
    app_id = re.search("([^/]+)(?=/[^/]+/?$)", link).group(0)
    results[app_id] = {"name": name, "description": description, "categories": categories, "link": link}
    printProgressBar(i+1, len(driver.find_elements_by_css_selector('.css-187scic-LargeHitContainer')), prefix = 'Progress:', suffix = 'Complete', length = 50)
print("Completed reading data from the list page! Starting to crawl item pages.")

# Initial call to print 0% progress
printProgressBar(0, len(results), prefix = 'Progress:', suffix = 'Complete', length = 50)
# go to each of the plugin pages and gather data from there
for i, key in enumerate(results, start = 1):
    driver.get(results[key]["link"])
    
    log.write("Row {} : {}".format(i, results[key]["link"]))
    
    results[key]["vendor_name"] = get_field_text_if_exists(driver, '.plugin-vendor-name')
    results[key]["total_installs"] = get_field_text_if_exists(driver, ".plugin-active-installs-total")
    results[key]["total_reviews"] = get_field_text_if_exists(driver, ".plugin-rating-summary .badge")
    results[key]["has_free_trial"] = get_field_text_if_exists(driver, '.primary-hosting-choice')
    results[key]["is_paid"] = get_field_text_if_exists(driver, '.secondary-hosting-choice')
    results[key]["is_free"] = get_field_text_if_exists(driver, ".free-addon-text")
    results[key]["support_status"] = get_field_text_if_exists(driver, ".plugin-support-status")
    results[key]["is_jira_service"] = get_field_text_if_exists(driver, ".plugin-jira-comp")

    try:
        # pricing = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#cloud-pricing .pup-pricing-block-amount")))
        for idx, r in enumerate(driver.find_elements_by_css_selector("#cloud-pricing .pup-pricing-block-amount"), start = 1):
            results[key]["pricing_cloud_{}".format(idx)] = r.get_attribute("innerText")
    except TimeoutException:
        pass
    
    try:
        server_pricing = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#server-pricing .amount strong")))
        for idx, r in enumerate(driver.find_elements_by_css_selector("#server-pricing .amount strong"), start = 1):
            results[key]["pricing_server_{}".format(idx)] = r.get_attribute("innerText")
    except TimeoutException:
        pass

    with open("data.csv", "a") as f:    
        w = csv.DictWriter(f, header)
        w.writerow(results[key])

    printProgressBar(i + 1, len(results), prefix = 'Progress:', suffix = 'Complete', length = 50)

driver.quit()
