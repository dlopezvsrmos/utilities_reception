from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.config.db_connection import cursor
from src.utilities.portal_base import PortalBase
from datetime import date





class Arkansas(PortalBase):

    def __init__(self,vendor_id, property_id, portal_user_id, portal_password_id, portal_submit_id):
        PortalBase.__init__(self,vendor_id, property_id, portal_user_id, portal_password_id, portal_submit_id)

    def execute(self, property_id, vendor_id):
        PortalBase.login(self)
        self.arkansas_water_portal(property_id, vendor_id)
    
    
    def arkansas_water_portal(self, property_id, vendor_id):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "title")))
        finally:
            self.driver.get("https://myaccount.carkw.com/css/account/accountList")
            cursor.execute(f"SELECT account_number FROM utility_accounts WHERE property = '{property_id}' AND utility_provider = '{vendor_id}'")

            values = cursor.fetchall()
            for account_number in values:
                cursor.execute(f"SELECT abbreviation FROM property WHERE id = '{property_id}'")
                property_abbreviation = cursor.fetchone()[0]
                invoice_number = str(date.today()).replace("-", "")
                link = f"/css/account/getAccount/{account_number[0]}"
                self.driver.get("https://myaccount.carkw.com" + link)
                download = "/css/billPrint/retrieve/currentBill"
                self.driver.get("https://myaccount.carkw.com" + download)
                self.driver.get("https://myaccount.carkw.com/css/account/accountList")
                
                PortalBase.save_file(self, property_abbreviation, invoice_number, account_number)

              
def main():
    portal = Arkansas("139", "21", "username", "password", "submit")
    portal.execute("139", "21")

if __name__ == "__main__":
    main()
