from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

binary_path="C:\selenium_driver_chrome\chromedriver.exe"
# binary_path="C:\Program Files\Google\Chrome\Application\chrome.exe"
service=Service(binary_path)
# driver = webdriver.Chrome(service=service)

# driver = webdriver.Chrome(executable_path=binary_path)
# url = "https://tixcraft.com/"
# driver.get(url)
# time.sleep(15)
# driver.quit()