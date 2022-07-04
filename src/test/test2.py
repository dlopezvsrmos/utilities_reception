from src.config.db_connection import cursor
from datetime import date

property_id = 130
vendor_id = 26


cursor.execute(f"SELECT account_number FROM utility_accounts WHERE property = '{property_id}' AND utility_provider = '{vendor_id}'")

accounts = cursor.fetchall()


for item in accounts[0:1]:
    print(item[0])