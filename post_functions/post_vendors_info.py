import csv
import db_structure as connection


with open('post_functions/account_list_2.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    collection = connection.vendors_col
    
    vendors_document = {
    "property_id":[],
    "vendor_name": "Central Arkansas Water",
    "type": "Water",
    "login1": {
        "username": "timbers@wehnermultifamily.com",
        "password": "Water*999",
        "accounts": [],
        }
    }
    document = {"login1": {
                    "username": "timbers@wehnermultifamily.com",
                    "password": "Water*999",
                    "accounts": [],
            }}
    
    for i in csv_reader:
        document['login1']['accounts'].append(i[0])
    
    #collection.insert_one(vendors_document)
    collection.update_one({"vendor_name": "Central Arkansas Water"}, {"$set": document})