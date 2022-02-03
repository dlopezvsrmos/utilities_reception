import csv
import db_structure as connection


with open('properties_list.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    collection = connection.vendors_col
    
    properties_document = {
    "types": {
        "water": [],
        "electricity": [],
        "gas": [],
        "trash": [],
        "telephone_internet": [],
        }
    }
    
    for i in csv_reader:
        properties_document['name']= i[0]
        collection.insert_one(properties_document)

