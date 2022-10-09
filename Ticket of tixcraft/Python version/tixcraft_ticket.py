# -*- coding: utf-8 -*-
from selenium import webdriver
from chromedriver_py import service
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from twocaptcha import TwoCaptcha
from twocaptcha.api import ApiException, NetworkException
from twocaptcha.solver import ValidationException
from selenium.common.exceptions import TimeoutException


def Buy_tickets(url): # 買票準備(Google登入)
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

def Get_Ticket_Prepare(): # 選擇時間場次
    GetTicket = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div/ul/li[1]/a'))
    )
    GetTicket.click()
    Ticket_Section = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="gameList"]/table/tbody/tr/td[4]/input'))
    )
    Ticket_Section.click()
    time.sleep(0.5)
    return

def Select_Ticket_Area(): # 選擇價格區
    Ticket_Area = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="group_0"]/li[1]')) #特區
        # //*[@id="group_0"]/li[2]
        # //*[@id="group_0"]/li[3]
    )
    Ticket_Area.click()

    time.sleep(0.5)
    return

def Select_Ticket_Quantity(): # 選擇票數
    Ticket_Quantity = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="TicketForm_ticketPrice_01"]')) 
    )
    select = Select(Ticket_Quantity)
    # Now we have many different alternatives to select an option.
    select.select_by_index(4)
    select.select_by_value('4') #Pass value as string

    Checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="TicketForm_agree"]'))
    )
    Checkbox.click()

    #驗證碼
    captcha_filename = get_captcha_screenshot()
    print("captcha_filename:",captcha_filename)
    solved_captcha = send_captcha(captcha_filename)
    print("solved_captcha:",solved_captcha)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="TicketForm_verifyCode"]'))
    )
    login_form_verify = driver.find_element(By.CSS_SELECTOR, '#TicketForm_verifyCode')
    login_form_verify.send_keys(solved_captcha['code'])

    Ticket_Submit=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="ticketPriceSubmit"]'))
    )
    Ticket_Submit.click()

    time.sleep(0.5)
    return

def get_captcha_screenshot(): # 驗證碼截圖
    # takes a screenshot and returns the filename captcha.png

    element =WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#yw0"))
    )

    fname = "captcha.png"
    element.screenshot(fname)
    # time.sleep(1)
    return fname

def send_captcha(fname): # 辨識驗證碼
    solver = TwoCaptcha(apiKey='91dec2ea4cee1487b6735e575021e1bd',pollingInterval=3)
    print('balance left USD', solver.balance())
    start = time.time()
    try:
        result = solver.normal(fname)
        end = time.time()
        print('result',result)
        print('elapsed time：', str(round(end - start, 2)))
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

def Select_Ticket_Pament(): #選擇價格區
    Ticket_Pament = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="PaymentForm_payment_id_36"]'))
    )
    Ticket_Pament.click()

    # Ticket_Sumit = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//*[@id="submitButton"]'))
    # )
    # Ticket_Sumit.click()

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
    # options.add_argument("--profile-directory=Profile 2")
    options.add_argument('--profile-directory=Default')

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

