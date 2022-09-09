# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import json
import time

def get_cookies(url,driver):
    #獲取cookies並保存到本地
    driver.get(url)
    dictCookie=driver.get_cookies()
    jsonCookie=json.dumps(dictCookie)
    with open('tixcraft_cookies.txt','w') as f:
        f.write(jsonCookie)
    print('Cookie 保存成功')

def load_tixcraft(driver):
    # 從本地讀取並刷新頁面
    with open('tixcraft_cookies.txt','r',encoding='utf8') as f:
        ListCookie=json.loads(f.read())

    for cookie in ListCookie:
        cookie_dict={
            'domain':'.tixcraft.com',
            'name':cookie.get('name'),
            'value':cookie.get('value'),
            'expires':'',
            'path':'/',
            'httpOnly':False,
            "HostOnly":False,
            'Secure':False
        }
        driver.add_cookie(cookie_dict)
    driver.refresh()

chromedriver = 'C:\selenium_driver_chrome\chromedriver.exe'

driver = webdriver.Chrome(chromedriver)
driver.set_window_position(0,0) #瀏覽器位置
driver.maximize_window #瀏覽器大小


# url = 'https://tixcraft.com'
url = 'https://tixcraft.com/login/google'
driver.get(url)
loginname=("lynn3693257@gmail.com")#欲登入之google帳號
gmailpassword=("QWEasd0257")#欲登入之google帳號密碼
# =============================================================================
# Selenium被Google阻擋範例
# 如果你是用webdriver所開啟的瀏覽器
# Google登入一律當作你要做壞事
# 會進行登入阻擋
# 叫你去用正常瀏覽器登入
# =============================================================================
emailid = driver.find_element(By.NAME, "identifier")
emailid.send_keys(loginname)
driver.find_element(By.XPATH,'//*[@id="identifierNext"]/content/span').click()


# =============================================================================
# get_cookies(url,driver)
# time.sleep(15)
# 
# load_tixcraft(driver)
# =============================================================================

