import csv
import db_structure as connection


with open('account_list.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    collection = connection.vendors_col
    
    vendors_document = {
    "property_id":[],
    "vendor_name": "Central Arkansas Water",
    "type": "Water",
    "login0": {
        "username": "invoices@wehnermultifamily.com",
        "password": "water2021",
        "accounts": [],
        }
    }
    
    for i in csv_reader:
        vendors_document['login0']['accounts'].append(i[0])
    
    collection.insert_one(vendors_document)