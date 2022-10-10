from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
from dotenv import load_dotenv
from twocaptcha import TwoCaptcha
from twocaptcha.api import ApiException, NetworkException
from twocaptcha.solver import ValidationException

binary_path="C:\selenium_driver_chrome\chromedriver.exe"
service=Service(binary_path)

def Train_Ticket_Prepare(driver,url,User_StartStation,User_TargetStation,User_Id,User_TrainNumber,Target_Date): # 買票準備(相關資訊填寫)
    driver.get(url)
    # 填入訂票資訊
    # 1.身份證號
    Passenger_Id = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="pid"]'))
    )
    Passenger_Id.send_keys(User_Id)
    # 2.起程站
    StartStation = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="startStation1"]'))
    )
    StartStation.send_keys(User_StartStation)
    # 2.到達站
    TargetStation = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="endStation1"]'))
    )
    TargetStation.send_keys(User_TargetStation)
    # 3.欲搭乘班次
    TrainNumber = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="trainNoList1"]'))
    )
    TrainNumber.send_keys(User_TrainNumber)
    # 3.欲搭乘日期
    RideDate = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="rideDate1"]'))
    )
    # 將預設資訊清除
    RideDate.clear()
    RideDate.send_keys(Target_Date)

    # 點擊查詢按鈕
    Query = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="queryForm"]/div[5]/input'))
    )
    Query.click()

    time.sleep(0.5)

    return

def Train_Ticket_Confirm(driver):
    Train_Selection = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="queryForm"]/div[1]/table/tbody/tr[2]/td[10]/label'))
    )
    Train_Selection.click()

    Google_Captcha_Solve(driver)

    NextButton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="queryForm"]/div[2]/button[2]'))
    )
    NextButton.click()
    
    return

def Google_Captcha_Solve(driver):

    Google_Captcha= WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'g-recaptcha-response'))
    )
    # make input visible
    driver.execute_script("arguments[0].setAttribute('style','type: text; visibility:visible;');",Google_Captcha)
    # input the code received from 2captcha API
    solved_captcha = Captcha_Solver()
    Google_Captcha.send_keys(solved_captcha.get('code'))
    # hide the captch input
    driver.execute_script("arguments[0].setAttribute('style', 'display:none;');",Google_Captcha)

    return

def Captcha_Solver():
        try:
            load_dotenv()
            CAPTCHA_Key = os.getenv("CAPTCHA_API_KEY")
            Train_sitekey = os.getenv("Sitekey")
            website_url = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/queryTrain"
            solver = TwoCaptcha(apiKey=CAPTCHA_Key)
            print('Solving captcha...')
            result = solver.recaptcha(sitekey=Train_sitekey, url=website_url)
            print('result:', result)
            print('balance left USD', solver.balance())
            return result
        except ValidationException as e:
            # invalid parameters passed
            print(e)
            return e
        except NetworkException as e:
            # network error occurred
            print(e)
            return e
        except ApiException as e:
            # api respond with error
            print(e)
            return e
        except TimeoutException as e:
            # captcha is not solved so far
            print(e)
            return e

def Train_Ticket_Payment(driver): # 票種
    Train_Order = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="order"]/div[3]/button'))
    )
    Train_Order.click()

    return

if __name__ == '__main__':
     # 取出.env檔案填寫的資訊
    load_dotenv()
    User_StartStation = os.getenv("StartStation_Setting")
    User_TargetStation = os.getenv("TargetStation_Setting")
    User_Id = os.getenv("User_Info")
    User_TrainNumber= os.getenv("Train_No")
    Target_Date = os.getenv("Timeing_Setting")
    print(f'The StartStation is: {User_StartStation}.')
    print(f'The TargetStation  is: {User_TargetStation}.')
    print(f'The user id is: {User_Id}.')
    print(f'The TrainNumber is: {User_TrainNumber}.')
    print(f'The Target Date is: {Target_Date}.')

    driver = webdriver.Chrome(service=service)
    url = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query"
    Train_Ticket_Prepare(url,User_StartStation,User_TargetStation,User_Id,User_TrainNumber,Target_Date)
    Train_Ticket_Confirm()
    Train_Ticket_Payment()