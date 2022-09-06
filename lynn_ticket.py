# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

chromedriver = "C:\selenium_driver_chrome\chromedriver.exe"
driver = webdriver.Chrome(chromedriver)
#driver.get('https://tixcraft.com/activity/game/19_GEM')#鄧紫琪網頁
#driver.get("https://tixcraft.com/activity/game/19_YJS")#測試位置區域1
driver.get("https://tixcraft.com/activity/game/19_BLACKPINK")#測試位置區域2
#driver.get("https://tixcraft.com/activity/game/19_LEO37SOSS")
driver.set_window_position(0,0) #瀏覽器位置
driver.maximize_window #瀏覽器大小
next_btn = driver.find_element_by_css_selector('.btn-next')
next_btn.click()

el=driver.find_element_by_link_text("會員登入")
el.click()

url = 'https://tixcraft.com/login/google'
driver.get(url)
loginname=("lynn3693257@gmail.com")#欲登入之google帳號
gmailpassword=("kiaebnib")#欲登入之google帳號密碼
emailid=driver.find_element_by_name("identifier")
emailid.send_keys(loginname)
driver.find_element_by_xpath('//*[@id="identifierNext"]/content/span').click()

password = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))
)
password.send_keys(gmailpassword)
driver.find_element_by_id("passwordNext").click()


ticket= WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="group_0"]/li[2]')))
if not ticket.is_selected():
    ticket.click()


wait = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_id("TicketForm_ticketPrice_01"))

select = Select(wait)
# Now we have many different alternatives to select an option.
select.select_by_index(4)
select.select_by_value('4') #Pass value as string

checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "TicketForm_agree")))
if not checkbox.is_selected():
    checkbox.click()
    
verifyCode= WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="TicketForm_verifyCode"]')))
if not verifyCode.is_selected():
    verifyCode.click()