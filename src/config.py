mappings = {
    "settings": {
        "number_of_shards": 1
    },
    "mappings": {
        "properties": {
            'plate': { "type": "text"},
            'state': { "type": "text"},
            'license_type': { "type": "text"},
            'violation': { "type": "text"},
            'violation_time': { "type": "text"},
            'precint': { "type": "text"},
            'county': { "type": "text"},
            'issuing_agency': { "type": "text"},
            'violation_status': { "type": "text"},
            'summons_number': { "type": "float"},
            'fine_amount': { "type": "float"},
            'penalty_amount': { "type": "float"},
            'interest_amount': { "type": "float"},
            'reduction_amount': { "type": "float"},
            'payment_amount': { "type": "float"},
            'amount_due': { "type": "float"},
            'issue_date': { "type": "text"},
            'judgment_entry_date': { "type": "text"},
            'url': {"type": "url"}
        }
    }
}