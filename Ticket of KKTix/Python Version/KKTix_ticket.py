from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pickle
from selenium.common.exceptions import UnexpectedAlertPresentException,NoAlertPresentException

def Login_Prepare(driver,url,User_Name,User_Password): # 買票準備(登入)
    driver.get(url)

    # User_Name=("lynn3693257@gmail.com")#欲登入之帳號
    # User_Password=("lynn36930728")#欲登入之帳號密碼
    
    # 登入帳號
    Login_Name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="user_login"]'))
    )
    Login_Name.send_keys(User_Name)
    # 登入密碼
    Login_Password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="user_password"]'))
    )
    Login_Password.send_keys(User_Password)
    # 登入送出紐
    Login_Submit = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="new_user"]/input[3]'))
    )
    Login_Submit.click()

    # 獲取cookies
    seleniumSaveCookie()

    time.sleep(0.5)
    return


def seleniumSaveCookie(): #save cookie function
    try:
        pickle.dump(driver.get_cookies(), open("cookie.pkl", "wb")) #writing in pickle file
        print('Cookie file successfully created.')
    except Exception as e:
        print(e)


def seleniumLoadCookie(): #load cookie function
    try:
        cookie = pickle.load(open("cookie.pkl", "rb")) #loading from pickle file
        for i in cookie:
            driver.add_cookie(i)
        print('Cookies added.')
    except Exception as e:
        print(e)

def Target_Activity(driver,url,Section_Order): # 欲搶的活動
    driver.get(url)
    driver.delete_all_cookies()
    seleniumLoadCookie()
    driver.get(url)

    # 欲搶的活動場次
    Tarket_Session = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, Section_Order))
    )
    Tarket_Session.click()

    return

def Target_Order(driver,Target_Price,User_Ticket_Count): # 票種和張數選擇

    Price_Order= '/html/body/div[3]/div[4]/div/div/div[5]/div[2]/div[3]/div[' + Target_Price + ']/div'
    print('欲搶票價的Full X path:',Price_Order)

    # 票種定位和Id - 因為增加按鈕的Xpath會隨著上層的Id做變化，所以需要先取出Id
    Ticet_Id=driver.find_element(By.XPATH,Price_Order).get_attribute('Id')    
    print('Ticket Id is %s' % Ticet_Id)
    # 增加按鈕的Xpath
    Ticet_AddButon_Xpath = '//*[@id="' + Ticet_Id +'"]/div/span[4]/button[2]'
    print('Ticet AddButon Xpath is %s' % Ticet_AddButon_Xpath)

    Target_click = int(User_Ticket_Count)
    count = 1

    while count <= Target_click:
        try:
            AddButton = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, Ticet_AddButon_Xpath))
            )
            AddButton.click()
            print("Button clicked #", count+1)
            count += 1
            time.sleep(0.1)

        except TimeoutException:
            break
    
    Agree_Terms = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="person_agree_terms"]'))
    )
    Agree_Terms.click()

    print('進入問題頁面，請使用者開始作答問題....')
    Question_Page_url = driver.current_url
    print('Question_Page_url:',Question_Page_url)

    while True:
        get_url = driver.current_url
        print('get_url:',get_url)
        if get_url == Question_Page_url:
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
            return Question_Page_url

    # Next_Step = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//*[@id="registrationsNewApp"]/div/div[5]/div[4]/button'))
    # )
    # Next_Step.click()

def Seat_Selection(driver):
    # 確認座位
    PopUp_Window = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="infoModal"]/div[2]/div/div[3]/button'))
    )
    PopUp_Window.click()

    # 確認座位
    Seat_Confirm = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="registrationsShowApp"]/div[2]/div/div/div/ng-include[2]/div/div/div/div[3]/div/button'))
    )
    Seat_Confirm.click()

    # 確認座位 again
    Seat_Confirm_Again = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="registrationsShowApp"]/div[2]/div/div/div/ng-include[2]/div/div/div/div[3]/div/div/div/div[1]/a'))
    )
    Seat_Confirm_Again.click()

    return

def Fulfill_Sheet(driver):
    # 公開頁面顯示參加活動 *checkbox*
    Agree_Terms = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="registrations_controller"]/div[4]/div[2]/div/div[4]/label/input'))
    )
    Agree_Terms.click()

    print('進入表單填寫頁面，請使用者開始輸入身分證字號和點選同意選項....')
    Fulfill_Sheet_url = driver.current_url
    print('表單填寫頁面網址:',Fulfill_Sheet_url)

    while True:
        get_url = driver.current_url
        print('get_url:',get_url)
        if get_url == Fulfill_Sheet_url:
            print('使用者填寫中....')
            try:
                alert = driver.switch_to.alert
            except NoAlertPresentException:
                continue
            else:
                print("Warning: unexpected alert ({})".format(alert.text))
                alert.accept()
        else:
            print('偵測到使用者填寫完成....')
            return

    # 確認表單資料
    # Next_Step = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//*[@id="registrations_controller"]/div[4]/div[2]/div/div[5]/a'))
    # )
    # Next_Step.click()

    return

def Ticket_Pament(driver,Question_Page_url,Target_url,User_Id,Section_Order,Target_Price,User_Ticket_Count):

    Pament_Url = driver.current_url

    # 點選取票方式
    GetTicket_Method = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="registrations_controller"]/div[4]/div[2]/div/div[1]/form/div[2]/table/tbody[2]/tr[1]/td/div/div/div/ul/li[1]/div/div/label/input'))
    )
    GetTicket_Method.click()

    # User_Id=("B223084553")#使用者身分證字號
    # 輸入使用者身分證字號
    Identity_Number = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="registrations_controller"]/div[4]/div[2]/div/div[1]/form/div[2]/table/tbody[2]/tr[1]/td/div/div/div/ul/li[1]/div/div/div/div/div/div/input'))
    )
    Identity_Number.send_keys(User_Id)

    # 確認訂單並繳費
    Order_Confirm = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="registrations_controller"]/div[4]/div[2]/div/div[1]/form/div[3]/span/button'))
    )
    Order_Confirm.click()


    while True:
        get_url = driver.current_url
        print('get_url:',get_url)
        if get_url == Pament_Url:
            print('使用者尚在取票繳費頁面....')
            try:
                alert = driver.switch_to.alert
            except NoAlertPresentException:
                continue
            else:
                print("Warning: unexpected alert ({})".format(alert.text))
                alert.accept()
        else:
            print('偵測到換頁....')
            Retry_Detect(driver,get_url,Question_Page_url,Target_url,Section_Order,Target_Price,User_Ticket_Count,User_Id)
            return

def Retry_Detect(driver,Waiting_url,Question_Page_url,Target_url,Section_Order,Target_Price,User_Ticket_Count,User_Id): #若被踢出要重try
    get_url = driver.current_url
    print('重試偵測啟動')
    print('現在網頁網址為 %s' % get_url)

    while True:
        get_url = driver.current_url
        if get_url == Waiting_url:
            print('網址轉圈等待中，程式維持不動....')
            print('重新偵測網頁網址為 %s' % get_url)
            try:
                alert = driver.switch_to.alert
            except NoAlertPresentException:
                continue
            else:
                print("Warning: unexpected alert ({})".format(alert.text))
                alert.accept()
            time.sleep(0.5)
        elif get_url == Target_url:
            print('偵測網頁網址為 %s' % get_url)
            print('重新執行搶票')
            Target_Activity(driver,Target_url,Section_Order)
            Target_Order(driver,Target_Price,User_Ticket_Count)
            Fulfill_Sheet(driver)
            Ticket_Pament(driver,Question_Page_url,Target_url,User_Id)
        elif get_url == Question_Page_url:
            print('偵測網頁網址為 %s' % get_url)
            print('請使用者重新回答問題....')
            Target_Order(driver,Target_Price,User_Ticket_Count)
            Fulfill_Sheet(driver)
            Ticket_Pament(driver,Question_Page_url,Target_url,User_Id)
        else:
            print('重新偵測網頁網址為 %s' % get_url)
            print('成功搶到票，請使用者進行付款選擇....')

            return


if __name__ == '__main__':

    binary_path="C:\selenium_driver_chrome\chromedriver.exe"
    service=Service(binary_path)

    driver = webdriver.Chrome(service=service)
    Login_url = "https://kktix.com/users/sign_in?back_to=https%3A%2F%2Fkktix.com%2F"
    Login_Prepare(driver,Login_url) # 買票準備(登入) - Step 0.0

    Target_url = "https://nicemedia.kktix.cc/events/time-leap1st"
    Target_Activity(driver,Target_url)  # 欲搶的活動  - Step 0.1

    Question_Page_url=Target_Order(driver) # 選擇票種和張數 - Step1

    # 劃位 - Step2 *若為電腦配位，這頁會跳過*
    # Seat_Selection(driver)
    # 填寫表單 - Step3
    Fulfill_Sheet(driver)
    # 取票繳費 - Step4
    Ticket_Pament(driver)

    time.sleep(300)