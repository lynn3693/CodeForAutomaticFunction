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
            'domain':'.pchome.com.tw',
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



url = 'https://ecvip.pchome.com.tw/login/v3/login.htm?rurl=https://24h.pchome.com.tw/index/v1'
driver.get(url)
loginname=("0934038548")#欲登入之帳號
gmailpassword=("lynn36930728")#欲登入之密碼
# =============================================================================
# Selenium被Google阻擋範例
# 如果你是用webdriver所開啟的瀏覽器
# Google登入一律當作你要做壞事
# 會進行登入阻擋
# 叫你去用正常瀏覽器登入
# =============================================================================
emailid = driver.find_element(By.XPATH,'//*[@id="loginAcc"]')
emailid.send_keys(loginname)
emailpassword = driver.find_element(By.XPATH,'//*[@id="loginPwd"]')
emailpassword.send_keys(gmailpassword)
driver.find_element(By.XPATH,'//*[@id="btnLogin"]').click()

driver.get('https://24h.pchome.com.tw/prod/DYAJCX-1900C885P?fq=/S/DYAJJV')
driver.find_element(By.XPATH,'//*[@id="ButtonContainer"]/button').click()




# time.sleep(15)
# get_cookies(url,driver)
# time.sleep(15)

# load_tixcraft(driver)


