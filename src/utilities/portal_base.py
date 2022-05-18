from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from src.config.db_connection import cursor
from selenium.webdriver.common.by import By
import os, requests, json
from datetime import date


class PortalBase:

    def __init__(self):
        self.chrome_options = Options()
        #self.chrome_options.add_argument("--headless")
        self.chrome_options = webdriver.ChromeOptions()
        self.prefs = {'download.default_directory' : '/home/diego/Desktop/MOS/utilities_reception/downloads/'}
        self.chrome_options.add_experimental_option('prefs', self.prefs)
        self.path = "/home/diego/Desktop/MOS/utilities_reception/downloads/"

        self.url = "https://mmp.worldwidemos.com/api/utility-invoices"
        self.today = str(date.today())
        self.info = {"emission_date" : f"{self.today}", "reception_date":f"{self.today}"}
        self.info = json.dumps(self.info)
        self.payload={'data': f'{self.info}'}
        self.headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjMsImlhdCI6MTY1MTY3NjU2OSwiZXhwIjoxNjU0MjY4NTY5fQ.dKygACaG3HyXTItLp6tVnqB0kpMRQ4ST_qie0n30feE'}
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=self.chrome_options)

    def execute(self, vendor_id):
        cursor.execute(f"SELECT id,	provider_name, e_bill_login_url FROM utility_providers WHERE id = '{vendor_id}'")
        information = cursor.fetchone()
        return information

    def login(self, vendor_id, property_id, portal_user_id, portal_password_id, portal_submit_id):
        login_link = self.execute(vendor_id)[2]
        self.driver.get(login_link)
        cursor.execute(f"SELECT e_bill_username,e_bill_password	FROM utility_accounts WHERE property = '{property_id}' AND utility_provider = '{vendor_id}'")
        credentials = cursor.fetchone()
        user = credentials[0]
        password = credentials[1]
        self.driver.find_element(By.ID, portal_user_id).send_keys(user)
        self.driver.find_element(By.ID, portal_password_id).send_keys(password)
        self.driver.find_element(By.ID, portal_submit_id).click()

    def save_file(self, property_abbreviation, invoice_number, account_number):
        file_downloaded = os.listdir(self.path)
        name = f"1A_{property_abbreviation}_{invoice_number}-{account_number[0]}.pdf"
        os.rename(f"{self.path}{file_downloaded[0]}", f"{self.path}{name}")
        file_path = f"{self.path}{name}"
        files = [('files.1',(name, open(file_path,'rb'),'application/pdf'))]
        response = requests.request("POST", self.url, headers=self.headers, data=self.payload, files=files)
        print(response.text)
        os.remove(file_path)