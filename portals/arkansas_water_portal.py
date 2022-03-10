from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os, boto3, sys
from dotenv import load_dotenv

sys.path.insert(0, "/home/diego/Desktop/utilities_reception/")
from post_functions import db_structure as connection

load_dotenv()

ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
AWS_REGION = os.environ.get("AWS_REGION")

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY, region_name=AWS_REGION)

s3_connection = session.client('s3')
# ENV variables
# TODO: find a way to handle file without downloading it


#chrome_options = Options()
#chrome_options.add_argument("--headless")

class Portal:

    def __init__(self):
        self.bucket_name = "utilities-reception"
        self.path = "/home/diego/Desktop/utilities_reception/downloads"
        self.chrome_options = webdriver.ChromeOptions()
        self.prefs = {'download.default_directory' : '/home/diego/Desktop/utilities_reception/downloads'}
        self.chrome_options.add_experimental_option('prefs', self.prefs)
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=self.chrome_options)

    def execute(self):
        self.driver.get("https://myaccount.carkw.com/css/public/login/form")
        login_username = self.driver.find_element(By.ID, "username").send_keys("timbers@wehnermultifamily.com")
        login_password = self.driver.find_element(By.ID, "password").send_keys("Water*999")
        self.driver.find_element(By.ID, "submit").click()
        self.arkansas_water_portal("Timbers", "Central Arkansas Water", "login1")
    
    def arkansas_water_portal(self, property_name, vendor_name, login_type):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "title")))
        finally:
            self.driver.get("https://myaccount.carkw.com/css/account/accountList")
            document = connection.vendors_col.find_one({"vendor_name": vendor_name})
            accounts = document[login_type]["accounts"]

            for account_number in accounts[0:3]:
                link = f"/css/account/getAccount/{account_number}"
                self.driver.get("https://myaccount.carkw.com" + link)
                download = "/css/billPrint/retrieve/currentBill"
                self.driver.get("https://myaccount.carkw.com" + download)
                self.driver.get("https://myaccount.carkw.com/css/account/accountList")

                file_downloaded = os.listdir(self.path)
                os.rename(f"{self.path}/{file_downloaded[0]}", f"{self.path}/{account_number}.pdf")
                file_path = f"{self.path}/{account_number}.pdf"
                file_name = f"{account_number}.pdf"
                file_uploaded = s3_connection.upload_file(file_path, self.bucket_name, file_name, ExtraArgs={'ContentType': 'application/pdf', "ContentDisposition": "inline"})
                url = f"https://utilities-reception.s3.amazonaws.com/{file_name}"
                os.remove(file_path)


def main():
    portal = Portal()
    portal.execute()

if __name__ == "__main__":
    main()
