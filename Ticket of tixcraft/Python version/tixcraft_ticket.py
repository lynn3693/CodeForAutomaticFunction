# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

def Buy_tickets(driver,url): # 買票準備(Google登入)
    driver.get(url)
    LoginArea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/ul/li[3]/a"))
    )
    LoginArea.click()
    Google_Login = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="loginGoogle"]'))
    )
    Google_Login.click()

    time.sleep(0.5)
    return

def Get_Ticket_Prepare(driver,Section_Order): # 選擇時間場次
    # 點選立即購票
    GetTicket = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div/ul/li[1]/a'))
    )
    GetTicket.click()
    # 點選場次
    Ticket_Section = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, Section_Order))
    )
    Ticket_Section.click()
    time.sleep(0.5)
    return

def Select_Ticket_Area(driver): # 選擇價格區
    Ticket_Area = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="group_0"]/li[1]')) #特區第一欄
        # //*[@id="group_0"]/li[2] #特區第2欄
        # //*[@id="group_0"]/li[3] #特區第3欄
    )
    Ticket_Area.click()

    time.sleep(0.5)
    return

def Select_Ticket_Quantity(driver,Ticket_Count): # 選擇票數
    Ticket_Quantity = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="TicketForm_ticketPrice_01"]')) 
    )
    select = Select(Ticket_Quantity)
    # Now we have many different alternatives to select an option.
    select.select_by_index(int(Ticket_Count))
    select.select_by_value(Ticket_Count) #Pass value as string

    Checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="TicketForm_agree"]'))
    )
    Checkbox.click()

    time.sleep(0.5)
    return

def Select_Ticket_Pament(driver):
    Ticket_Pament = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="PaymentForm_payment_id_36"]'))
    )
    Ticket_Pament.click()

    Ticket_Sumit = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="submitButton"]'))
    )
    Ticket_Sumit.click()

    time.sleep(0.5)
    return

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # 步驟1獲取到的User Data路徑
    # options.add_argument(r'--user-data-dir=C:\Users\Admin\AppData\Local\Google\Chrome\User Data')
    options.add_argument(r'--user-data-dir=C:\Users\USER\AppData\Local\Google\Chrome\User Data')
    # 步驟2獲取到的--profile-directory值
    # 查詢方式:chrome://version/
    # options.add_argument("--profile-directory=Profile 2")
    options.add_argument('--profile-directory=Default')

    binary_path="C:\selenium_driver_chrome\chromedriver.exe"
    service=Service(binary_path)

    driver = webdriver.Chrome(options=options, service=service)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    url = "https://tixcraft.com/activity/detail/22_aayan1120"
    Buy_tickets(url)
    Get_Ticket_Prepare()
    Select_Ticket_Area()
    Select_Ticket_Quantity()
    Select_Ticket_Pament()

