## Data Gathering And Analysis

This is a project for data crawling (given a web link) and exploring the gathered data to answer some data analysis questions.

**Stack**: Python, Selenium

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
