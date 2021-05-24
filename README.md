# open-parking-camera-violation
I. Source: 

Link to the dataset: https://data.cityofnewyork.us/City-Government/Open-Parking-and-Camera-Violations/nc67-uf89

Link to Socrata Open Parking and Camera Violations (OPCV) API: https://dev.socrata.com/foundry/data.cityofnewyork.us/nc67-uf89

II. Description/Summary:

1. About the dataset

This dataset, owned by NYC Open Data, is provided by Department of Finance. Each row is a open parking and camera violation issued. Original dataset has over 62 million rows, which are violations issued from 2016. There are 19 columns in the dataset and new and open violations are updated weekly on Sunday. 

2. About the project

Using EC2 instance, I write a python script that queries >199k rows of data through Socrata Open Data API then push them to AWS ElasticSearch. That way, I don't have to store any data into my virtual machine, and instead, I stream them directly to ES and analyze and visualize them on Kibana. 

    My dashboard addresses the following topics: 
    
        - Most popular violations
        - Top 20 states with the highest average fine amount and their average reduction amount
        - The average fine amount, payment amount and interest amount by year
        - Most common violation status
        - Issuing Agencies with most violations issued 

III. Instructions on how to build and run the docker image
  
1. Create a Dockerfile in "project01" folder that installs Python 3.9 then use WORKDIR command to create and change directory to a new folder named "/app" inside the container to store all the files needed to run the application. 

2. Then copy the requirements.txt file and all of the python code files in /src folder including main.py, elastic_helper.py, and config.py into the current directory (/app) using COPY command. 

3. Then, pip install all of the requirements/ dependencies (request and sodapy modules)

4. Use ENTRYPOINT command and pass "python" and "main.py" to run the code

5. To build a container based on the docker image, type this on your command line : "docker build -t bigdata1:1.0 project01" – make sure you're in the parent folder of "project01" folder

6. Then to run the application, type this: 

docker run \
 -e DATASET_ID=nc67-uf89 \
 -e APP_TOKEN={APP_TOKEN} \
 -e ES_HOST={ES_HOST} \
 -e ES_USERNAME={ES_USERNAME} \
 -e ES_PASSWORD={ES_PASSWORD} \
 --network="host" \
 bigdata1:1.0 --num_pages=3 --page_size=2
 
 with: 
 
 DATASET_ID: "nc67-uf89" is the ID for this dataset, retrieved from Socrata API link above 
 
 APP_TOKEN: get this from NYC Open Data (https://data.cityofnewyork.us/profile/edit/developer_settings)
 
 ES_HOST: get the endpoint link when you create an Elastic Search domain 
 
 ES_USERNAME: your Elastic Search username
 
 ES_PASSWORD: your Elastic Search password
 
 Note: If using terminal on local machine, review Docker Desktop installation instruction here: https://www.docker.com/products/docker-desktop
 
 
 
