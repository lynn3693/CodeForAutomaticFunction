# -*- coding: utf-8 -*-
from msilib.schema import Condition
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from selenium.common.exceptions import UnexpectedAlertPresentException,NoAlertPresentException
import re

def Tixcraft_GoogleLogin(driver,url): # 買票準備(Google登入)
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

def Select_Ticket_TimeAndSession(driver,Section_Order): # 選擇時間場次
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

def Select_Ticket_Area(driver,Target_PriceList,User_Ticket_Count): # 選擇價格區

    for Target_Price in Target_PriceList:
        print('目標價格編號為: %s' % Target_Price)
        Target_Area='//*[@id="group_'+ str(Target_Price) + '"]'
        print('目標價格所屬Group為: %s' % Target_Area)
        AreaInfo_List=driver.find_element(By.XPATH, Target_Area).get_attribute('innerHTML')
        AreaId_List = re.findall('id=\"(.*?)\"',AreaInfo_List)
        print('AreaId List: %s' % AreaId_List)
        Seat_Count_Dictionary = {}
        for AreaId in AreaId_List:
            Seat_XpathId='//*[@id=\"'+ AreaId + '\"]/font'
            print('Seat_XpathId: %s' % Seat_XpathId)
            Seat=driver.find_element(By.XPATH, Seat_XpathId).get_attribute('innerHTML')
            print('座位狀態: %s' % Seat)
            Seat_Count=re.search(r'\d+', Seat)
            print('搜尋剩餘座位數量: %s' % Seat_Count)
            if Seat_Count:
                Remain_Seat= Seat_Count.group(0)
                print('剩餘座位:',Remain_Seat)
                if int(Remain_Seat) > int(User_Ticket_Count):
                    Seat_Count_Dictionary[AreaId] = int(Remain_Seat)
                else:
                    Seat_Count_Dictionary[AreaId] = 0
            print('Seat_Count_Dictionary:',Seat_Count_Dictionary)

    if len(Seat_Count_Dictionary) > 0:
        Choose_Element = max(Seat_Count_Dictionary, key=Seat_Count_Dictionary.get)
        print('目標選擇: %s' % Choose_Element)
        Seat_XpathId='//*[@id=\"'+ Choose_Element + '\"]/font'
        Choose_Ticket = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, Seat_XpathId))
        )
        Ticket_Area_url = driver.current_url
        Choose_Ticket.click()
        return Ticket_Area_url
    else:
        print('目標價格皆沒有座位，開始刷新頁面')
        driver.refresh()
        time.sleep(0.5)
        Select_Ticket_Area(driver,Target_PriceList,User_Ticket_Count)

    time.sleep(0.5)
    return Ticket_Area_url

def Select_Ticket_Quantity(driver,url,Section_Order,Ticket_Count,Area_url,Target_PriceList,User_Ticket_Count,Target_Mode="False"): # 選擇票數

    Ticket_Quantity = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/form/div[1]/table/tbody/tr/td[2]/select')) 
    )
    select = Select(Ticket_Quantity)
    # Now we have many different alternatives to select an option.
    select.select_by_index(int(Ticket_Count))
    select.select_by_value(Ticket_Count) #Pass value as string

    Checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="TicketForm_agree"]'))
    )
    Checkbox.click()

    while True:
        try:
            alert = driver.switch_to.alert
        except NoAlertPresentException:
            get_url = driver.current_url
            if get_url == "https://tixcraft.com/ticket/order":
                Retry_Detect(driver,url,Section_Order,Ticket_Count,Area_url,Target_PriceList,User_Ticket_Count,Target_Mode)
                return
        else:
            print("Warning: unexpected alert ({})".format(alert.text))
            alert.accept()
            Select_Ticket_Quantity(driver,url,Section_Order,Ticket_Count,Area_url,Target_PriceList,User_Ticket_Count)
            return

def Retry_Detect(driver,url,Section_Order,Ticket_Count,Area_url,Target_PriceList,User_Ticket_Count,Target_Mode="False"): #若被踢出要重try
    get_url = driver.current_url
    print('重試偵測啟動')
    print('現在網頁網址為 %s' % get_url)

    while True:
        get_url = driver.current_url
        if get_url == "https://tixcraft.com/ticket/order":
            print('拓元網址轉圈等待中，程式維持不動....')
            print('重新偵測網頁網址為 %s' % get_url)
            try:
                alert = driver.switch_to.alert
            except NoAlertPresentException:
                continue
            else:
                print("Warning: unexpected alert ({})".format(alert.text))
                alert.accept()
            time.sleep(0.5)
        elif get_url == "https://tixcraft.com/ticket/checkout":
            print('重新偵測網頁網址為 %s' % get_url)
            print('成功搶到票，請使用者進行付款選擇....')
            # Select_Ticket_Pament(driver)
            return
        elif get_url == url:
            print('偵測網頁網址為 %s' % get_url)
            print('重新執行搶票')
            if Target_Mode=="False":
                Select_Ticket_TimeAndSession(driver,Section_Order)
                Select_Ticket_Area(driver,Target_PriceList,User_Ticket_Count)
                Select_Ticket_Quantity(driver,url,Section_Order,Ticket_Count,Area_url,Target_PriceList,User_Ticket_Count)
            else:
                Select_Ticket_TimeAndSession(driver,Section_Order)
                Question_page(url,Section_Order,driver)
                Select_Ticket_Quantity(driver,url,Section_Order,Ticket_Count,Area_url,Target_PriceList,User_Ticket_Count,Target_Mode)
        elif get_url == Area_url:
            print('偵測網頁網址為 %s' % get_url)
            print('重新開始偵測座位狀態....')
            Select_Ticket_Area(driver,Target_PriceList,User_Ticket_Count)
            Select_Ticket_Quantity(driver,url,Section_Order,Ticket_Count,Area_url,Target_PriceList,User_Ticket_Count)

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

def Question_page(url,Section_Order,driver):
    print('進入問題頁面，請使用者開始作答問題....')
    Question_Page_url = driver.current_url
    print('Question_Page_url:',Question_Page_url)
    while True:
        get_url = driver.current_url
        print('get_url:',get_url)
        if get_url == url:
            print('偵測到使用者作答問題失敗，網頁已回到前一頁....')
            Select_Ticket_TimeAndSession(driver,Section_Order)
        elif get_url == Question_Page_url:
            print('使用者作答問題中....')
            try:
                alert = driver.switch_to.alert
            except NoAlertPresentException:
                continue
            else:
                print("Warning: unexpected alert ({})".format(alert.text))
                alert.accept()
        else:
            print('偵測到使用者作答問題成功....')
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

    url = "https://tixcraft.com/ticket/area/22_WuBaiOPR/11325"
    # Buy_tickets(url)
    # Get_Ticket_Prepare()
    Select_Ticket_Area(url,driver)
    # Select_Ticket_Quantity()
    # Select_Ticket_Pament()
    # Retry_Detect(driver,url)

