from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.config.db_connection import cursor
from src.utilities.portal_base import PortalBase
from datetime import date


class Green(PortalBase):

    def __init__(self,vendor_id, property_id, portal_user_id, portal_password_id, portal_submit_id):
        PortalBase.__init__(self,vendor_id, property_id, portal_user_id, portal_password_id, portal_submit_id)

    def execute(self, property_id, vendor_id):
        PortalBase.login(self)
        self.green_mountain_portal(property_id, vendor_id)
    
    
    def green_mountain_portal(self, property_id, vendor_id):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "title")))
        finally:
            self.driver.get("https://www.businessportal.greenmountain.com/login.htm?")
            cursor.execute(f"SELECT account_number FROM utility_accounts WHERE property = '{property_id}' AND utility_provider = '{vendor_id}'")

            values = cursor.fetchall()
            

            for account_number in values:
                cursor.execute(f"SELECT abbreviation FROM property WHERE id = '{property_id}'")
                property_abbreviation = cursor.fetchone()[0]
                invoice_number = str(date.today()).replace("-", "")
                self.driver.execute_script(f"getPayBill('{account_number[0]}').click()")
                self.driver.get("https://www.businessportal.greenmountain.com/resources/protected/payBillDetails.htm")
                
                table = self.driver.find_element(By.ID, "transTbody")
                table.find_element_by_tag_name("a").click()
                
                PortalBase.save_file(self, property_abbreviation, invoice_number, account_number)

              
def main():
    portal = Green("139", "21", "username", "password", "logonButton")
    portal.execute("139", "21")

if __name__ == "__main__":
    main()