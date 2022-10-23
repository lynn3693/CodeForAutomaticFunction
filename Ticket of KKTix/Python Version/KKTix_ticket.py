from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pickle




binary_path="C:\selenium_driver_chrome\chromedriver.exe"
service=Service(binary_path)

def Login_Prepare(driver,url): # 買票準備(登入)
    driver.get(url)

    User_Name=("lynn3693257@gmail.com")#欲登入之帳號
    User_Password=("lynn36930728")#欲登入之帳號密碼
    
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

def Tarket_Activity(driver,url): # 欲搶的活動
    driver.get(url)
    driver.delete_all_cookies()
    seleniumLoadCookie()
    driver.get(url)

    # 欲搶的活動場次
    Tarket_Session = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/ul/li[2]/div/a'))
    )
    Tarket_Session.click()

    return

def Tarket_Order(driver): # 票種和張數選擇

    # 票種定位和Id - 因為增加按鈕的Xpath會隨著上層的Id做變化，所以需要先取出Id
    Ticet_Id=driver.find_element(By.XPATH,'/html/body/div[3]/div[4]/div/div/div[5]/div[1]/div[3]/div[1]/div').get_attribute('Id')    
    print('Ticket Id is %s' % Ticet_Id)
    # 增加按鈕的Xpath
    Ticet_AddButon_Xpath = '//*[@id="' + Ticet_Id +'"]/div/span[3]/button[2]'
    print('Ticet AddButon Xpath is %s' % Ticet_AddButon_Xpath)

    Target_click = 2
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

    Next_Step = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="registrationsNewApp"]/div/div[5]/div[4]/button'))
    )
    Next_Step.click()

    return




if __name__ == '__main__':

    binary_path="C:\selenium_driver_chrome\chromedriver.exe"
    service=Service(binary_path)

    driver = webdriver.Chrome(service=service)
    Login_url = "https://kktix.com/users/sign_in?back_to=https%3A%2F%2Fkktix.com%2F"
    Login_Prepare(driver,Login_url) # 買票準備(登入)

    Target_url = "https://rockempire.kktix.cc/events/nightwish2023new"
    Tarket_Activity(driver,Target_url)  # 欲搶的活動

    Tarket_Order(driver) # 票種和張數選擇

    time.sleep(300)