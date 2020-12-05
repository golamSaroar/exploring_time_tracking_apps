import csv

fields = [ 'app_name', 'app_description', 'app_installs', 'app_test' ]
dw     = { '1': { 'app_name' : 2, 'app_description' : 3, 'app_test': 1, 'app_installs' : 4 },
           '2': { 'app_name' : 1, 'app_description' : 2, 'app_test': 4, 'app_installs' : 3 },
           '3': { 'app_name' : 1, 'app_description' : 3, 'app_test': 2, 'app_installs' : 4 }
        }

with open("test_output.csv", "w") as f:
    w = csv.DictWriter( f, fields )
    w.writeheader()
    for key,val in dw.items():
        row = val
        w.writerow(row)

# TRIED PRICES
# for i, r in enumerate(driver.find_elements_by_css_selector("#cloud-pricing .pup-pricing-block-amount")):
#     try:
#         results[key]["app_pricing_cloud_{}".format(i)] = r.get_attribute("innerText")
#     except (IndexError, NoSuchElementException):
#         results[key]["app_pricing_cloud_{}".format(i)] = ""

# try:
#     server_pricing = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#server-pricing .amount strong")))
#     for i, r in enumerate(driver.find_elements_by_css_selector("#server-pricing .amount strong")):
#         try:
#             results[key]["app_pricing_server_{}".format(i)] = r.get_attribute("innerText")
#         except (IndexError, NoSuchElementException):
#             results[key]["app_pricing_server_{}".format(i)] = ""
# except TimeoutException:
#     continue