import argparse
import os
import math
import requests
import sys


from sodapy import Socrata
from datetime import datetime
from elastic_helper import (ElasticHelperException, 
                            try_create_index,
                            try_delete_index,
                            insert_doc
                            )
                            
from config import mappings as es_mappings

DATASET_ID = os.environ.get("DATASET_ID") 
APP_TOKEN = os.environ.get("APP_TOKEN") 
ES_HOST = os.environ.get("ES_HOST") 
ES_USERNAME = os.environ.get("ES_USERNAME") 
ES_PASSWORD = os.environ.get("ES_PASSWORD") 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Process parking violation ticket")
    parser.add_argument('--page_size', type = int, help = 'how many rows to get per page', required = True)
    parser.add_argument('--num_pages', type = int, help = 'how many pages to get in total')
    args = parser.parse_args(sys.argv[1:])
    
    client = Socrata(
        "data.cityofnewyork.us", 
        APP_TOKEN,
        )
    
    
     #   STEP 1: try to create an index in ES
    try:
        try_create_index(
            "parking",
            ES_HOST,
            mappings = es_mappings,
            es_user = ES_USERNAME,
            es_pw = ES_PASSWORD,
            )
            
    except ElasticHelperException as e:
        print("Index already exists! Skipping")
        print(f"{e}")
    
    # STEP 2: query the data and get rows 
    
    total_rows = int(client.get(DATASET_ID,select = 'COUNT(*)')[0]['COUNT'])
    limit = args.page_size
    num_pages = args.num_pages
    if num_pages is None:
        num_pages = math.ceil(total_rows/limit)
    
    for page in range(0,num_pages):
        rows = client.get(DATASET_ID, limit=limit, offset = page*limit, order =":id")
    # STEP 3: convert the row data into the correct types as needed
        for row in rows:
            try:
                row['fine_amount'] = float(row.get('fine_amount', 0.0)),
                row['interest_amount'] = float(row.get('interest_amount', 0.0)),
                row['reduction_amount'] = float(row.get('reduction_amount', 0.0)),
                row['payment_amount'] = float(row.get('payment_amount', 0.0)),
                row['amount_due'] = float(row.get('amount_due', 0.0)),
                row['summons_number'] = float(row.get('summons_number', 0.0)),
                row['issue_date'] = datetime.strptime(row['issue_date'],'%m/%d/%Y').isoformat()
            except Exception as e:
                print(f"SKIPPING! Failed to transform row: {row}: Reason: {e}")
                continue
            
        #STEP 4: POST this data to ES
            try:
                ret = insert_doc(
                    "parking",
                    ES_HOST,
                    data = row,
                    es_user = ES_USERNAME,
                    es_pw = ES_PASSWORD,
                )
                print(ret)
            except ElasticHelperException as e:
                print(e)
            
    # try:
    #     try_delete_index(
    #         "parking1",
    #         ES_HOST,
    #         mappings = es_mappings,
    #         es_user = ES_USERNAME,
    #         es_pw = ES_PASSWORD,
    #         )
            
    # except ElasticHelperException as e:
    #     print("Index is already deleted! Skipping")
    #     print(f"{e}")


    
    
    
    