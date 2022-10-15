import tkinter as tk
from selenium import webdriver
import time
import datetime
from tkinter import messagebox
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from tixcraft_ticket import Buy_tickets,Get_Ticket_Prepare,Select_Ticket_Area,Select_Ticket_Quantity,Select_Ticket_Pament,get_captcha_screenshot,send_captcha


def Reservation_Checking():
    Today = datetime.datetime.now()
    Tomorrow = Today + datetime.timedelta(days=1)

    if Year.get() == "":
        Reserve_Year = Tomorrow.year
        print('Default Year:',Reserve_Year)
    else:
        Reserve_Year = int(Year.get())
        print('Year:',Reserve_Year)

    if Min.get() == "":
        Reserve_Min =  0
        print('Default Minute:',Reserve_Min)
    else:
        Reserve_Min = int(Min.get())
        print('Minute:',Reserve_Min)

    Input_List = [len(Month.get()),len(Day.get()),len(Hour.get()),len(Ticket_Count.get())]

    Check_Result=index_withoutexception(Input_List,0)


    if  Check_Result == -1:
        Reserve_Month = int(Month.get())
        print('Month:',Reserve_Month)

        Reserve_Day = int(Day.get())
        print('Day:',Reserve_Day)

        Reserve_Hour = int(Hour.get())
        print('Hour:',Reserve_Hour)
    else:
        messagebox.showinfo('showinfo', '預約搶票時間輸入有誤，必填項目:?月?日?時和搶票張數，請確認後重新輸入')

    User_Ticket_Count=Ticket_Count.get()
    
    Main_tixcraft_ticket(Reserve_Year, Reserve_Month, Reserve_Day, Reserve_Hour, Reserve_Min,User_Ticket_Count)
    
    return

def Main_tixcraft_ticket(Reserve_Year, Reserve_Month, Reserve_Day, Reserve_Hour, Reserve_Min,User_Ticket_Count):
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

    User_url=url.get()

    Buy_tickets(driver,User_url)

    startTime = datetime.datetime(Reserve_Year, Reserve_Month, Reserve_Day, Reserve_Hour, Reserve_Min, 0)
    while datetime.datetime.now() < startTime:
        time.sleep(1)
    print('Program now starts on %s' % startTime)
    print('Executing...')

    Get_Ticket_Prepare(driver)
    Select_Ticket_Area(driver)
    Select_Ticket_Quantity(driver,User_Ticket_Count)
    Select_Ticket_Pament(driver)
    time.sleep(300)

    return

def Input_Checking():
    User_url=url.get()

    Input_List = [len(User_url)]

    Check_Result=index_withoutexception(Input_List,0)


    if  Check_Result == -1:
        Reservation_Checking()
    else:
        messagebox.showinfo('showinfo', '沒有輸入搶票網址，請重新輸入')

    return

def index_withoutexception(self,i):
    try:
        return self.index(i)
    except:
        return -1

if __name__ == '__main__':
    User_UI = tk.Tk()   # 建立 tkinter 視窗物件
    User_UI.title('拓元自動搶票程式') # 設定標題
    width = 700
    height = 500
    left = 0
    top = 0
    User_UI.geometry(f'{width}x{height}+{left}+{top}')  # 定義視窗的尺寸和位置

    tk.Label(User_UI, text='欲搶票的活動網址:',font=('Arial',20,'bold')).place(relx=0, rely=0)
    url = tk.StringVar()   # 建立文字變數
    url.set('')            # 一開始設定沒有內容
    tk.Entry(User_UI, textvariable=url,width=50).place(relx=0.35, rely=0.015)  # 放入 Entry
    tk.Label(User_UI, text='輸入範例:https://tixcraft.com/activity/detail/22_aayan1120',font=('Arial',12,'bold')).place(relx=0.35, rely=0.055)

    tk.Label(User_UI, text='預約日期與時間設定:',font=('Arial',20,'bold')).place(relx=0, rely=0.1)
    
    Year = tk.StringVar()   # 建立文字變數
    Year.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='年',font=('Arial',20,'bold')).place(relx=0.18, rely=0.2)
    tk.Entry(User_UI, textvariable=Year,width=6).place(relx=0.1, rely=0.215)  # 放入 Entry

    Month = tk.StringVar()   # 建立文字變數
    Month.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='月',font=('Arial',20,'bold')).place(relx=0.33, rely=0.2)
    tk.Entry(User_UI, textvariable=Month,width=6).place(relx=0.25, rely=0.215)  # 放入 Entry

    Day = tk.StringVar()   # 建立文字變數
    Day.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='日',font=('Arial',20,'bold')).place(relx=0.48, rely=0.2)
    tk.Entry(User_UI, textvariable=Day,width=6).place(relx=0.4, rely=0.215)  # 放入 Entry

    Hour = tk.StringVar()   # 建立文字變數
    Hour.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='時',font=('Arial',20,'bold')).place(relx=0.63, rely=0.2)
    tk.Entry(User_UI, textvariable=Hour,width=6).place(relx=0.55, rely=0.215)  # 放入 Entry

    Min = tk.StringVar()   # 建立文字變數
    Min.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='分',font=('Arial',20,'bold')).place(relx=0.78, rely=0.2)
    tk.Entry(User_UI, textvariable=Min,width=6).place(relx=0.7, rely=0.215)  # 放入 Entry

    Ticket_Count = tk.StringVar()   # 建立文字變數
    Ticket_Count.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='欲購買張數:',font=('Arial',20,'bold')).place(relx=0, rely=0.3)
    tk.Entry(User_UI, textvariable=Ticket_Count,width=6).place(relx=0.25, rely=0.32)  # 放入 Entry

    Submit_Button = tk.Button(User_UI, text='送出', font=('Arial',20), width=5, command=lambda: Input_Checking() ).place(relx=0.4, rely=0.4)

    User_UI.mainloop()  # 放在主迴圈中