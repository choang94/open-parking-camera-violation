import requests
from requests.auth import HTTPBasicAuth
# from datetime import datetime

class ElasticHelperException(Exception):
    pass

def try_create_index(index_name, host, mappings=None,es_user=None, es_pw=None):
    if not es_user or not es_pw:
        raise ElasticHelperException("Your username and password is required")
        
    if mappings is None or len(mappings.keys()) == 0:
        raise ElasticHelperException("Must specify at least a mapping")
        
    try:
        resp = requests.put(
            f"{host}/{index_name}", 
            auth = HTTPBasicAuth(es_user, es_pw),
            json = mappings,
        )
        resp.raise_for_status()
        print("Successfully created index!")
    except Exception:
        raise ElasticHelperException("Index already exists!")
 
        
def try_delete_index(index_name,host,mappings=None,es_user=None,es_pw=None):
    if not es_user or not es_pw:
        raise ElasticHelperException("Your username and password is required")
        
    if mappings is None or len(mappings.keys()) == 0:
        raise ElasticHelperException("Must specify at least a mapping")
        
    try:
        resp = requests.delete(
            f"{host}/{index_name}", 
            auth = HTTPBasicAuth(es_user, es_pw),
            json = mappings,
        )
        resp.raise_for_status()
        print("Successfully deleted index!")
    except Exception:
        raise ElasticHelperException("Index is already deleted!")
    
        
def insert_doc(index_name, host, data=None, es_user=None, es_pw=None):
    if not es_user or not es_pw:
        raise ElasticHelperException("Your username and password is required")
    
    if data is None or len(data.keys()) == 0:
        raise ElasticHelperException("This data is empty")
        
    try:
        resp = requests.post(
            f"{host}/{index_name}/_doc", 
            auth = HTTPBasicAuth(es_user, es_pw),
            json = data,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        raise ElasticHelperException(f"Failed to create document: {e}")        

# def data_formatting(row):
#     for key, value in row.items():
#         if 'amount' in key:
#             row[key] = float(value)
#         elif 'number' in key:
#             row[key] = int(value)            
#         elif 'date' in key:
#             row[key] = datetime.strptime(row[key], '%m/%d/%Y').isoformat()
        
        
        
        
        
        
        
                