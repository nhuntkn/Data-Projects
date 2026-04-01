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

- [Dataset Used](#dataset-used)
- [Technologies](#technologies)
- [Data Pipeline Architecture](#data-pipeline-architecture)
- [Data Modeling](#data-modeling)
- [Step 1: Cleaning and Transformation](step-1-cleaning-and-transformation)
- [Step 2: Storage](step-2-storage)
- [Step 3: ETL/ Orchestration](#step-3-etlorchestration)
- [Step 4: Analytics](#step-4-analytics)
- [Step 5: Dashboard](#step-5-dashboard)

## Dataset Used

This project uses the Bureau of Infrastructure and Transport Research Economics (BITRE) data, which provides basic details on road traffic crash fatalities in Australia include state, incident date/time, crash type, bus/heavy rigid truck/articulated truck involvement, speed limit, road user, gender, age, national remoteness areas, SA4 name, national LGA name, national road type, Christmas/Easter period. Each fatality record shows a killed person.

More infomation about dataset can be found in the following links:
- Website: [https://datahub.roadsafety.gov.au/progress-reporting/monthly-road-deaths](https://datahub.roadsafety.gov.au/progress-reporting/monthly-road-deaths#anchor-download-data:~:text=new%20tab/window)
- Data Dictionary: [https://datahub.roadsafety.gov.au/sites/default/files/documents/](https://datahub.roadsafety.gov.au/sites/default/files/documents/Australian%20Road%20Deaths%20Database%20Data%20Dictionary%20December%202025.pdf)
- Raw Data (CSV): https://github.com/nhuntkn/Data-Projects/blob/Australia-Road-Death-Project/Australia%20Road%20Death%20Project/fatalities_feb2026.csv

## Technologies

The following technologies are used to build this project:
- Language: Python, SQL
- Extraction and transformation: Jupyter Notebook, Google BigQuery
- Storage: Google Cloud Storage
- Orchestration: [Mage AI](https://www.mage.ai/)
- Dashboard: [Looker Studio](https://lookerstudio.google.com/)

## Data Pipeline Architecture

<img width="750" height="281" alt="image" src="https://github.com/user-attachments/assets/d4646d78-a3b0-4a62-b868-ec59c2d3e979" />

Files in the following stages:
- Step 1: Cleaning and transformation - [Fatalities_Engineering.ipynb](https://github.com/nhuntkn/Data-Projects/blob/Australia-Road-Death-Project/Australia%20Road%20Death%20Project/Fatalities%20Data%20Engineering.ipynb)
- Step 2: Storage
- Step 3: ETL, Orchestration - Mage: [Load](https://github.com/nhuntkn/Data-Projects/blob/Australia-Road-Death-Project/Australia%20Road%20Death%20Project/Mage/fatality_load_data.py), [Transform](https://github.com/nhuntkn/Data-Projects/blob/Australia-Road-Death-Project/Australia%20Road%20Death%20Project/Mage/fatality_transformer.py), [Export](https://github.com/nhuntkn/Data-Projects/blob/Australia-Road-Death-Project/Australia%20Road%20Death%20Project/Mage/fatality_export.py).
- Step 4: Analytics - [SQL script](https://github.com/nhuntkn/Data-Projects/blob/Australia-Road-Death-Project/Australia%20Road%20Death%20Project/SQL_Script.sql)
- Step 5: [Dashboard](https://github.com/nhuntkn/Data-Projects/blob/Australia-Road-Death-Project/Australia%20Road%20Death%20Project/AUS-Road-Deaths-Dashboard.pdf).

## Data Modeling

The datasets are designed using the principles of fact and dim data modelling concepts.
<img width="1277" height="841" alt="image" src="https://github.com/user-attachments/assets/e6556e3b-7125-4c60-9a35-f340a11c55b8" />


## Step 1: Cleaning and Transformation

In this step, I loaded the CSV file into Jupyter Notebook and carried out data cleaning and transformation activities prior to organizing them into fact and dim tables.

Script link: [Fatalities Data Engineering.ipynb](https://github.com/nhuntkn/Data-Projects/blob/Australia-Road-Death-Project/Australia%20Road%20Death%20Project/Fatalities%20Data%20Engineering.ipynb)

Here's the specific cleaning and transformation tasks that were performed:
1.  Create *Time of Day* column.
2. Converted *Time* column into DateTime type.
3. Handle the value *-9* as missing/unknown values.
4. Remove all suplicates.
5. Create *Holiday Flag* and *Weekend Flag* columns.

<img width="1502" height="1084" alt="image" src="https://github.com/user-attachments/assets/4b37b629-647d-4ed9-9cd6-768a6b94e9d6" />
<img width="1499" height="697" alt="image" src="https://github.com/user-attachments/assets/22af3fc9-3649-4e1c-9d44-f2f3ba6c4903" />

After completing the above steps, I created the following fact and dimension tables below:

<img width="1495" height="957" alt="image" src="https://github.com/user-attachments/assets/8b9647d2-3926-40ac-9f1e-79c2b9156857" />
<img width="1496" height="894" alt="image" src="https://github.com/user-attachments/assets/a0956f79-7a91-41eb-944f-9b93fcc02625" />
<img width="1500" height="763" alt="image" src="https://github.com/user-attachments/assets/4711d887-e0c9-4912-8e3b-cb9db8993512" />

## Step 2: Storage

<img width="2203" height="674" alt="image" src="https://github.com/user-attachments/assets/70ebf302-7aea-4980-b241-cadce1c1c98f" />

## Step 3: ETL/Orchestration

<img width="2209" height="685" alt="Screenshot 2026-04-01 171343" src="https://github.com/user-attachments/assets/b0e5bc44-b96e-4dc1-8005-d317f847fea9" />

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
2. After that, I install the Mage AI library from the [Mage AI Github](https://github.com/mage-ai/mage-ai#using-pip-or-conda). Then, I create a new project called **aus-road-deaths-project**.
```
# Install Mage library
sudo pip3 install mage-ai

# Create new project
mage start demo_project
```
3. Next, I conduct orchestration in Mage by accessing the external IP address through a new tab. The link format is: ```<external IP address>:<port number>```

After that, I create a new pipeline with the following stages:
- Load: [fatality_load](https://github.com/nhuntkn/Data-Projects/blob/Australia-Road-Death-Project/Australia%20Road%20Death%20Project/Mage/fatality_load_data.py).
- Transform: [fatality_transformer](https://github.com/nhuntkn/Data-Projects/blob/Australia-Road-Death-Project/Australia%20Road%20Death%20Project/Mage/fatality_transformer.py).
- Export :[fatality_export](https://github.com/nhuntkn/Data-Projects/blob/Australia-Road-Death-Project/Australia%20Road%20Death%20Project/Mage/fatality_export.py).

<img width="2203" height="1190" alt="image" src="https://github.com/user-attachments/assets/9cca6ec6-98f8-4bdc-8a79-ced328324abb" />

Before executing the Load pipeline, I download credentials from Google API & Credentials and then update them accordingly in the ```io_config.yaml``` file within the same pipeline. This step is essential for granting authorization to access and load dta into Google BigQuery.

## Step 4: Analytics

After running the Load pipeline in Mage, the fact and dim tables are generated in Google BigQuery.

<img width="2484" height="1346" alt="image" src="https://github.com/user-attachments/assets/10c15566-7137-4172-b9fd-4e0370e46b51" />

Here's the additional analyses I performed:
1. Find the top 10 sa4_name_2021 based on the number of fatalities.
<img width="1421" height="1013" alt="Screenshot 2026-04-01 173401" src="https://github.com/user-attachments/assets/7cc07ab1-f63f-4e5d-804a-1000c4682d41" />

2. Find the time of day when pedestrians or pedal cyclists are most likely to be in danger.
<img width="1435" height="1021" alt="Screenshot 2026-04-01 173453" src="https://github.com/user-attachments/assets/73ba428b-69c0-4431-8266-fc5c3bada44d" />

3. Find national remoteness areas that have high fatality numbers.
<img width="1434" height="807" alt="Screenshot 2026-04-01 173626" src="https://github.com/user-attachments/assets/d96de298-2b6f-4565-8700-817a233b385e" />

## Step 5: Dashboard

After completing the analysis, I loaded the relevant tables into Looker Studio and created a dashboard, which you can view [here](https://lookerstudio.google.com/reporting/0c639afa-8178-4b63-9ec8-bcf70831b1aa).

<img width="930" height="1295" alt="Screenshot 2026-04-01 154944" src="https://github.com/user-attachments/assets/904f5935-3909-467d-b5c8-c54757f5a1c7" />

