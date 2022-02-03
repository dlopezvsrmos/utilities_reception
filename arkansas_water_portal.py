from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import shutil
import boto3
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
AWS_REGION = os.environ.get("AWS_REGION")

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY, region_name=AWS_REGION)

s3_connection = session.client('s3')

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(
    ChromeDriverManager().install(), chrome_options=chrome_options)

Initial_path = "/home/diego/Desktop/utilities/"


driver.get("https://myaccount.carkw.com/css/public/login/form")

login_username = driver.find_element_by_id("username").send_keys("invoices@wehnermultifamily.com")
login_password = driver.find_element_by_id("password").send_keys("water2021")

driver.find_element_by_id("submit").click()

    
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "title")))

finally:
    driver.get("https://myaccount.carkw.com/css/account/accountList")

    for i in csv_reader:

        link = f"/css/account/getAccount/{i[0]}"
        driver.get("https://myaccount.carkw.com" + link)
        download = "/css/billPrint/retrieve/currentBill"
        driver.get("https://myaccount.carkw.com" + download)
        driver.get("https://myaccount.carkw.com/css/account/accountList")
        name = f"{[0]}.pdf"
        filename = max([Initial_path + f for f in os.listdir(Initial_path)],key=os.path.getctime)
        shutil.move(filename,os.path.join(Initial_path,name))






