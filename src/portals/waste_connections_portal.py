from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv


chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : '/home/diego/Desktop/utilities_reception/downloads'}
chrome_options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(
    ChromeDriverManager().install(), chrome_options=chrome_options)#, chrome_options=chrome_options)


driver.get("https://www.wcicustomer.com/Login.aspx")

login_username = driver.find_element(By.ID, "cphMain_txtUserID").send_keys("Wehner1")
login_password = driver.find_element(By.ID, "cphMain_txtPassword").send_keys("Wehner1977")

driver.find_element(By.ID, "btnLogin").click()


try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "MainHeader_hlBillPay")))

finally:
    driver.get("https://www.wcicustomer.com/User/KubraContainer.aspx?lp=6")
    # TODO: Preguntar a Andrea a partir de que fecha se debe comenzar a extraer los datos.
    # TODO: Crear iteración a partir la lista de accounts y hacer la descarga de invoice.
    # TODO: Hacer el post dentro de MMP.