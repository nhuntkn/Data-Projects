# Australia Road Deaths Data Engineering End-to-End Project

## Objective

In this project, I designed and implemented an end-to-end data pipeline that consists of several stages:

1. Extracted data from Australian Government Bureau of Infrastructure and Transport Research Economics (BITRE) and loaded into Google Cloud Storage for further processing.

2. Transformed and modeled the data using fact and dimensional data modeling concepts using Python on Jupyter Notebook.

3. Using ETL concept, I orchestrated the data pipeline on Mage AI and loaded the transformed data into Google BigQuery.

4. Developed a dashboard on Looker Studio.

As this is a data engineering project, I primarily focus on the engineering aspect with a lesser emphasis on analytics and dashboard development.

The sections below will explain additional details on the technologies and files utilized.

## Table of Content

- Dataset Used
- Technologies
- Data Pipeline Architecture
- Data Modelling
- Step 1: Cleaning and Transformation
- Step 2: Storage
- Step 3: ETL/ Orchestration
- Step 4: Analytics
- Step 5: Dashboard

## Dataset Used

This project uses the Bureau of Infrastructure and Transport Research Economics (BITRE) data, which provides basic details on road traffic crash fatalities in Australia include state, incident date/time, crash type, bus/heavy rigid truck/articulated truck involvement, speed limit, road user, gender, age, national remoteness areas, SA4 name, national LGA name, national road type, Christmas/Easter period. Each fatality record shows a killed person.

More infomation about dataset can be found in the following links:
- Website: [https://datahub.roadsafety.gov.au/progress-reporting/monthly-road-deaths](https://datahub.roadsafety.gov.au/progress-reporting/monthly-road-deaths#anchor-download-data:~:text=new%20tab/window)
- Data Dictionary: [https://datahub.roadsafety.gov.au/sites/default/files/documents/](https://datahub.roadsafety.gov.au/sites/default/files/documents/Australian%20Road%20Deaths%20Database%20Data%20Dictionary%20December%202025.pdf)
- Raw Data (CSV):

## Technologies

The following technologies are used to build this project:
- Language: Python, SQL
- Extraction and transformation: Jupyter Notebook, Google BigQuery
- Storage: Google Cloud Storage
- Orchestration: [Mage AI](https://www.mage.ai/)
- Dashboard: [Looker Studio](https://lookerstudio.google.com/)

## Data Pipeline Architecture

Files in the following stages:
- Step 1: Cleaning and transformation - [Fatalities Data Engineering.ipynb](https://github.com/nhuntkn/Data-Projects/blob/Australia-Road-Death-Project/Australia%20Road%20Death%20Project/Fatalities%20Data%20Engineering.ipynb)
- Step 2: Storage
- Step 3: ETL, Orchestration - Mage: Extract, Transform, Load
- Step 4: Analytics - SQL script
- Step 5: Dashboard

## Data Modelling

The datasets are designed using the principles of fact and dim data modelling concepts.


## Step 1: Cleaning and Transformation

In this step, I loaded the CSV file into Jupyter Notebook and carried out data cleaning and transformation activities prior to organizing them into fact and dim tables.

Script link: [Fatalities Data Engineering.ipynb](https://github.com/nhuntkn/Data-Projects/blob/Australia-Road-Death-Project/Australia%20Road%20Death%20Project/Fatalities%20Data%20Engineering.ipynb)

Here's the specific cleaning and transformation tasks that were performed:
1.  Create *Time of Day* column.
2. Converted *Time* column into DateTime type.
3. Handle the value *-9* as missing/unknown values.
4. Remove all suplicates.
5. Create *Holiday Flag* and *Weekend Flag* columns.

After completing the above steps, I created the following fact and dimension tables below:


## Step 2: Storage

<img width="2203" height="674" alt="image" src="https://github.com/user-attachments/assets/70ebf302-7aea-4980-b241-cadce1c1c98f" />

## Step 3: ETL/Orchestration

1. Begin by lanching the SSH instance and running the following commands below to install the required libraries.
```
# Install python and pip 
sudo apt-get install update

sudo apt-get install python3-distutils

sudo apt-get install python3-apt

sudo apt-get install wget

wget https://bootstrap.pypa.io/get-pip.py

sudo python3 get-pip.py

# Install Google Cloud Library
sudo pip3 install google-cloud

sudo pip3 install google-cloud-bigquery

# Install Pandas
sudo pip3 install pandas
```
2. After that, I install the Mage AI library from the Mage AI Github. Then, I create a new project called **aus-road-deaths-project**.
```
# Install Mage library
sudo pip3 install mage-ai

# Create new project
mage start demo_project
```
3. Next, I conduct orchestration in Mage by accessing the external IP address through a new tab. The link format is: ```<external IP address>:<port number>```

After that, I create a new pipeline with the following stages:
- Extract:
- Transform:
- Load:

<img width="2203" height="1190" alt="image" src="https://github.com/user-attachments/assets/9cca6ec6-98f8-4bdc-8a79-ced328324abb" />

Before executing the Load pipeline, I download credentials from Google API & Credentials and then update them accordingly in the ```io_config.yaml``` file within the same pipeline. This step is essential for granting authorization to access and load dta into Google BigQuery.

## Step 4: Analytics

After running the Load pipeline in Mage, the fact and dim tables are generated in Google BigQuery.

Here's the additional analyses I performed:
1. Find the top 5 sa4_name_2021 based on the number of fatalities.

2. Find the time of day when pedestrians or pedal cyclists are most likely to be in danger.

3. Find national remoteness areas that have high fatality numbers.

## Step 5: Dashboard

After completing the analysis, I loaded the relevant tables into Looker Studio and created a dashboard, which you can view [here](https://lookerstudio.google.com/reporting/0c639afa-8178-4b63-9ec8-bcf70831b1aa).

<img width="930" height="1295" alt="Screenshot 2026-04-01 154944" src="https://github.com/user-attachments/assets/904f5935-3909-467d-b5c8-c54757f5a1c7" />

