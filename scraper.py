import csv
import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from log import write, print_progress_bar

URL = "https://marketplace.atlassian.com/search?category=Time%20tracking&product=jira"


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
items = driver.find_elements_by_css_selector('.css-187scic-LargeHitContainer')
print_progress_bar(0, len(items), prefix='Progress:', suffix='Complete', length=50)
# get data from the list page (given URL) and add to the dictionary
for i, result in enumerate(items):
    name = get_field_text_if_exists(result, '.css-r7ms9i-H3-baseHeadingsCss-baseHeadingsCss-h3Css-h3Css-NameHeader')
    description = get_field_text_if_exists(result, '.css-1lqn5mv-Body')
    categories = get_field_text_if_exists(result, '.css-1hj6rt6-CategoriesStyled')
    link = get_link_if_exists(result, '.css-tgmll2-linkCss-linkCss-HitLinkStyled-HitLinkStyled')

    app_id = re.search("([^/]+)(?=/[^/]+/?$)", link).group(0)
    results[app_id] = {"name": name, "description": description, "categories": categories, "link": link}

    print_progress_bar(i + 1, len(items), prefix='Progress:', suffix='Complete', length=50)

print("Completed reading data from the list page! Starting to crawl item pages.")

print_progress_bar(0, len(results), prefix='Progress:', suffix='Complete', length=50)
# go to each of the plugin pages and gather data from there
for i, key in enumerate(results, start=1):
    driver.get(results[key]["link"])

    write("Row {} : {}".format(i, results[key]["link"]))

    results[key]["vendor_name"] = get_field_text_if_exists(driver, '.plugin-vendor-name')
    results[key]["total_installs"] = get_field_text_if_exists(driver, ".plugin-active-installs-total")
    results[key]["total_reviews"] = get_field_text_if_exists(driver, ".plugin-rating-summary .badge")
    results[key]["has_free_trial"] = get_field_text_if_exists(driver, '.primary-hosting-choice')
    results[key]["is_paid"] = get_field_text_if_exists(driver, '.secondary-hosting-choice')
    results[key]["is_free"] = get_field_text_if_exists(driver, ".free-addon-text")
    results[key]["support_status"] = get_field_text_if_exists(driver, ".plugin-support-status")
    results[key]["is_jira_service"] = get_field_text_if_exists(driver, ".plugin-jira-comp")

    try:
        cloud_pricing = wait.until(EC.presence_of_all_elements_located((
            By.CSS_SELECTOR, "#cloud-pricing .pup-pricing-block-amount")))
        for idx, r in enumerate(driver.find_elements_by_css_selector("#cloud-pricing .pup-pricing-block-amount"),
                                start=1):
            results[key]["pricing_cloud_{}".format(idx)] = r.get_attribute("innerText")
    except TimeoutException:
        pass

    try:
        server_pricing = wait.until(EC.presence_of_all_elements_located((
            By.CSS_SELECTOR, "#server-pricing .amount strong")))
        for idx, r in enumerate(driver.find_elements_by_css_selector("#server-pricing .amount strong"), start=1):
            results[key]["pricing_server_{}".format(idx)] = r.get_attribute("innerText")
    except TimeoutException:
        pass

    with open("data.csv", "a") as f:
        w = csv.DictWriter(f, header)
        w.writerow(results[key])

    print_progress_bar(i + 1, len(results), prefix='Progress:', suffix='Complete', length=50)

driver.quit()
