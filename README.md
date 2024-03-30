## Atlassian Marketplace Time Tracking Apps Analytics

This GitHub repository contains code for scraping data from the Atlassian Marketplace for apps in the Time Tracking category, followed by performing analytics on the gathered data to answer specific questions.

### Project Overview

The project consists of two main steps:

1. **Gathering Data:**
   - Crawling the information of all the apps from [Atlassian Marketplace Time Tracking category](https://marketplace.atlassian.com/search?category=Time%20tracking&product=jira).
   - Parsing and structuring the data in a CSV file for further analysis.

2. **Analyzing Data:**
   - Understanding the distribution of the number of installs for the plugins in the time tracking category.
   - Investigating the potential relationship between the number of installs and the price of the plugins.
   - Identifying predictive features for the number of installs and proposing suitable methods for prediction.

**Stack**: Python, Selenium

### Repository Structure

- `data.csv`: The CSV file with the scraped and structured data.
- `scraper.py`: Python script for data scraping.
- `README.md`: Provides an overview of the project and instructions for usage.
- `requirements.txt`: Lists the dependencies required for running the code.
- [Colab Notebook](https://colab.research.google.com/drive/1bXFaXM6V7ufEIINa8l-bsFDn2b64nudW?usp=sharing#scrollTo=DEkeu-8SP5am): Contains the data analysis.

### Explaining the Dataset
 Column        | Meaning        
| ------------- |:-------------:
| name          | Name of the plugin 
| description   | Short description      
| categories    | Plugin category
| vendor_name      | Plugin vendor name 
| total_installs      | Number of installs      
| total_reviews | Number of reviews  
| has_free_trial      |  If Free Trial is available. Non-empty value ("Try it free"/"Get it now", etc) means positive, otherwise negative.  
| is_paid      | If plugin requires purchase. Non-empty value ("Buy it now"/"Purchase", etc) means positive, otherwise negative.        
| is_free | Non empty value means plugin is free, otherwise not.  
| support_status      | Two distinct values: Supported, and Unsupported. 
| is_jira_service      |     Non empty value means plugin is a Jira Service Management, otherwise not.  
| link | Plugin detail page link
| pricing_cloud_1      | Plugin price (cloud) for up to 10 users 
| pricing_cloud_2      | Plugin price (cloud) per person for 10-100 users      
| pricing_server_1 | Plugin price (server) for 10 users
| pricing_server_2      | Plugin price (server) for 25 users
| pricing_server_3      | Plugin price (server) for 50 users
| pricing_server_4 | Plugin price (server) for 100 users
| pricing_server_5 | Plugin price (server) for 250 users

The data has been intentionally inserted into the CSV file without modification. This should give us an idea how the
 data was shown on the website.  
However, we need to preprocess data for analysis. Those steps have been performed in the notebook.  

### How to Build
##### Clone the Repository
`git clone https://github.com/golamSaroar/exploring_time_tracking_apps.git`  
`cd exploring_time_tracking_apps`

##### Installing Requirements
The only dependency of this project is *Selenium*. However, let's setup a virtual env for the project.  
Create a virtual environment either using [venv](https://docs.python.org/3/tutorial/venv.html) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html). We will use python version 3.8.x 

- **Creating**: If you're using conda, run:
`conda create --name env python=3.8`  

- **Activating**: Once the environment is created, run:
`conda activate env`
 
- **Installing Dependencies**: From the project root directory, run:
`pip install -r requirements.txt`.

##### Run the Project
In the terminal, run `python scraper.py`
