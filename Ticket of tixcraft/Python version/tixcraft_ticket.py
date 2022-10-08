# -*- coding: utf-8 -*-
from selenium import webdriver
from chromedriver_py import service
from selenium_stealth import stealth
import time

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# # 步驟1獲取到的User Data路徑
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

url = "https://tixcraft.com/"
driver.get(url)
time.sleep(15)
driver.quit()

