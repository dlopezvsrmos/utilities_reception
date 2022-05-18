from src.config.db_connection import cursor
from datetime import date

property_id = 139
vendor_id = 21


cursor.execute(f"SELECT e_bill_username,e_bill_password	FROM utility_accounts WHERE property = '{property_id}' AND utility_provider = '{vendor_id}'")
credentials = cursor.fetchone()
user = credentials[0]
password = credentials[1]
print(user, password)