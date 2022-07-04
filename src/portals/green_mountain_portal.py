from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.config.db_connection import cursor
from src.utilities.portal_base import PortalBase
from datetime import date
from bs4 import BeautifulSoup
import time


class Green(PortalBase):

    def __init__(self,vendor_id, property_id, portal_user_id, portal_password_id, portal_submit_id):
        PortalBase.__init__(self,vendor_id, property_id, portal_user_id, portal_password_id, portal_submit_id)

    def execute(self):
        PortalBase.login(self)
        self.green_mountain_portal()
    
    
    def green_mountain_portal(self):
      
        self.driver.get("https://www.businessportal.greenmountain.com/login.htm?")
        cursor.execute(f"SELECT account_number FROM utility_accounts WHERE property = '{self.property_id}' AND utility_provider = '{self.vendor_id}'")

        accounts = cursor.fetchall()
        
        invoice = []
        for account_number in accounts[0:1]:
            cursor.execute(f"SELECT abbreviation FROM property WHERE id = '{self.property_id}'")
            property_abbreviation = cursor.fetchone()[0]
            invoice_number = str(date.today()).replace("-", "")

            self.driver.execute_script(f"getPayBill('{account_number[0]}')")
            time.sleep(4)
            
            page_html = self.driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
            table_items = soup.findAll(class_='wordbreak')

            for info in table_items:
                if info.find("a") != None:
                    invoice.append(info.find("a").get_text())

            print(self.driver)
            self.driver.execute_script(f"fetchInvoice('{invoice[0]}', {account_number[0]})")           
            #PortalBase.save_file(self, property_abbreviation, invoice_number, account_number)
              
def main():
    portal = Green("130", "26", "username", "password", "logonButton")
    portal.execute()

if __name__ == "__main__":
    main()