import tkinter as tk
from selenium import webdriver
import time
import datetime
from tkinter import messagebox
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from tixcraft_ticket import Tixcraft_GoogleLogin,Select_Ticket_TimeAndSession,Select_Ticket_Area,Select_Ticket_Quantity,Retry_Detect,Question_page

def Reservation_Checking():
    
    User_Session=Session_Value.get()
    print('User_Session:',User_Session)
    User_SelectSession=Session_Select.get()
    print('User_SelectSession:',User_SelectSession)

    if  User_Session == "單一場次":
        Section_Order='//*[@id="gameList"]/table/tbody/tr/td[4]/input'
        print('Section_Order:',Section_Order)
    else:
        Section_Order= '//*[@id="gameList"]/table/tbody/tr[' + User_SelectSession + ']/td[4]/input'
        print('Section_Order:',Section_Order)


    Target_PriceList = []
    if Target_Price1.get():
        print('Target_Price1:',Target_Price1.get())
        element= int(Target_Price1.get()) - 1
        if element not in Target_PriceList:
            Target_PriceList.append(element)

    if Target_Price2.get():
        print('Target_Price2:',Target_Price2.get())
        element= int(Target_Price2.get()) - 1
        if element not in Target_PriceList:
            Target_PriceList.append(element)

    if Target_Price3.get():
        print('Target_Price3:',Target_Price3.get())
        element= int(Target_Price3.get()) - 1
        if element not in Target_PriceList:
            Target_PriceList.append(element)
    print('Target_PriceList:',Target_PriceList)

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

    if Sec.get() == "":
        Reserve_Sec =  0
        print('Default Second:',Reserve_Sec)
    else:
        Reserve_Sec = int(Sec.get())
        print('Second:',Reserve_Sec)

    Input_List = [len(Month.get()),len(Day.get()),len(Hour.get()),len(Ticket_Count.get()),len(Target_PriceList)]
    Check_Result=index_withoutexception(Input_List,0)

    
    if  len(Month.get()) == 0 | len(Day.get()) ==0 :
        messagebox.showinfo('showinfo', '請輸入幾月幾號開搶')
    
    if  len(Hour.get()) ==0 :
        messagebox.showinfo('showinfo', '請輸入幾點開搶')

    if  len(Ticket_Count.get()) ==0 :
        messagebox.showinfo('showinfo', '請輸入搶票張數')

    if  len(Target_PriceList) == 0:
        messagebox.showinfo('showinfo', '請至少輸入一個目標價格編號')

    if  Check_Result == -1:
        Reserve_Month = int(Month.get())
        print('Month:',Reserve_Month)

        Reserve_Day = int(Day.get())
        print('Day:',Reserve_Day)

        Reserve_Hour = int(Hour.get())
        print('Hour:',Reserve_Hour)

    User_Ticket_Count=Ticket_Count.get()

    if  int(User_Ticket_Count) < 5:
        Main_tixcraft_ticket(Reserve_Year, Reserve_Month, Reserve_Day, Reserve_Hour, Reserve_Min,User_Ticket_Count,Section_Order,Target_PriceList)
    else:
        messagebox.showinfo('showinfo', '票數不可以超過4張')
    
    return

def Main_tixcraft_ticket(Reserve_Year, Reserve_Month, Reserve_Day, Reserve_Hour, Reserve_Min,User_Ticket_Count,Section_Order,Target_PriceList):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # 步驟1獲取到的User Data路徑
    User_Name=Name.get()
    Data_Dir = r'--user-data-dir=C:\Users\USER\AppData\Local\Google\Chrome\User Data'
    User_Data_Dir = Data_Dir.replace("USER", User_Name)
    # options.add_argument(r'--user-data-dir=C:\Users\Admin\AppData\Local\Google\Chrome\User Data')
    # options.add_argument(r'--user-data-dir=C:\Users\USER\AppData\Local\Google\Chrome\User Data')
    options.add_argument(User_Data_Dir)
    # 步驟2獲取到的--profile-directory值
    # 查詢方式:chrome://version/
    User_Data=Google_Data.get()
    Google_Profile= '--profile-directory=' + User_Data
    options.add_argument(Google_Profile)
    # options.add_argument("--profile-directory=Profile 2")
    # options.add_argument('--profile-directory=Default')

    binary_path="C:\selenium_driver_chrome\chromedriver.exe"
    service=Service(binary_path)

    driver = webdriver.Chrome(options=options, service=service)

    stealth(driver,
            languages=["zh-TW", "tw"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    User_url=url.get()

    Tixcraft_GoogleLogin(driver,User_url)

    startTime = datetime.datetime(Reserve_Year, Reserve_Month, Reserve_Day, Reserve_Hour, Reserve_Min, 0)
    while datetime.datetime.now() < startTime:
        time.sleep(1)
    print('Program now starts on %s' % startTime)
    print('Executing...')
    driver.refresh()
    time.sleep(0.5)

    Target_Mode=Question_Mode.get()
    print('Target_Mode is:',Target_Mode)
    if Target_Mode=="False":
        print('Executing program in normal mode...')
        Select_Ticket_TimeAndSession(driver,Section_Order)
        Ticket_Area_url=Select_Ticket_Area(driver,Target_PriceList,User_Ticket_Count)
        Select_Ticket_Quantity(driver,User_url,Section_Order,User_Ticket_Count,Ticket_Area_url,Target_PriceList,User_Ticket_Count)
        print('成功搶到票，程式進入休眠....')
    else:
        print('Executing program in question mode...')
        Select_Ticket_TimeAndSession(driver,Section_Order)
        Question_page(User_url,Section_Order,driver)
        Ticket_Area_url=Select_Ticket_Area(driver,Target_PriceList,User_Ticket_Count)
        Select_Ticket_Quantity(driver,User_url,Section_Order,User_Ticket_Count,Ticket_Area_url,Target_PriceList,User_Ticket_Count,Target_Mode)
        print('成功搶到票，程式進入休眠....')
    time.sleep(6000)

    return

def Input_Checking():
    User_url=url.get()
    User_Name=Name.get()
    User_Data=Google_Data.get()
    print('User_Name:',User_Name)
    print('User_Data:',User_Data)


    Google_Profile= '--profile-directory=' + User_Data
    print('Google_Profile:',Google_Profile)

    Input_List = [len(User_url),len(User_Name),len(User_Data)]

    Check_Result=index_withoutexception(Input_List,0)
    
    if  len(User_url) == 0:
        messagebox.showinfo('showinfo', '請輸入目標網址')

    if  len(User_Name) == 0:
        messagebox.showinfo('showinfo', '請輸入電腦User Name')
    
    if  len(User_Data) == 0:
        messagebox.showinfo('showinfo', '請輸入Google Profile Name')

    if  Check_Result == -1:
        Reservation_Checking()

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
    height = 900
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
    tk.Label(User_UI, text='*預設為今年',font=('Arial',12,'bold')).place(relx=0.08, rely=0.26)

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
    tk.Label(User_UI, text='*24小時制',font=('Arial',12,'bold')).place(relx=0.53, rely=0.27)

    Min = tk.StringVar()   # 建立文字變數
    Min.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='分',font=('Arial',20,'bold')).place(relx=0.78, rely=0.2)
    tk.Entry(User_UI, textvariable=Min,width=6).place(relx=0.7, rely=0.215)  # 放入 Entry
    tk.Label(User_UI, text='*預設為0',font=('Arial',12,'bold')).place(relx=0.68, rely=0.27)

    Sec = tk.StringVar()   # 建立文字變數
    Sec.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='秒',font=('Arial',20,'bold')).place(relx=0.93, rely=0.2)
    tk.Entry(User_UI, textvariable=Sec,width=6).place(relx=0.85, rely=0.215)  # 放入 Entry
    tk.Label(User_UI, text='*預設為0',font=('Arial',12,'bold')).place(relx=0.83, rely=0.27)

    Question_Mode = tk.StringVar()   # 建立文字變數
    Question_Mode.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='是否有問題要回答:',font=('Arial',20,'bold')).place(relx=0, rely=0.32)
    On_btn = tk.Radiobutton(User_UI, text='是',font=('Arial',12,'bold'),variable=Question_Mode, value='True').place(relx=0, rely=0.4)

    Off_btn = tk.Radiobutton(User_UI, text='否',font=('Arial',12,'bold'),variable=Question_Mode, value='False')
    Off_btn.select()
    Off_btn.place(relx=0.15, rely=0.4)

    Ticket_Count = tk.StringVar()   # 建立文字變數
    Ticket_Count.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='欲購買張數:',font=('Arial',20,'bold')).place(relx=0, rely=0.48)
    tk.Entry(User_UI, textvariable=Ticket_Count,width=6).place(relx=0.25, rely=0.49)  # 放入 Entry

    Target_Price1 = tk.StringVar()   # 建立文字變數
    Target_Price1.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='目標價格編號:',font=('Arial',20,'bold')).place(relx=0, rely=0.6)
    tk.Label(User_UI, text='第一目標',font=('Arial',12,'bold')).place(relx=0.28, rely=0.57)
    tk.Entry(User_UI, textvariable=Target_Price1,width=6).place(relx=0.3, rely=0.62)  # 放入 Entry

    Target_Price2 = tk.StringVar()   # 建立文字變數
    Target_Price2.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='第二目標',font=('Arial',12,'bold')).place(relx=0.43, rely=0.57)
    tk.Entry(User_UI, textvariable=Target_Price2,width=6).place(relx=0.45, rely=0.62)  # 放入 Entry

    Target_Price3 = tk.StringVar()   # 建立文字變數
    Target_Price3.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='第三目標',font=('Arial',12,'bold')).place(relx=0.58, rely=0.57)
    tk.Entry(User_UI, textvariable=Target_Price3,width=6).place(relx=0.6, rely=0.62)  # 放入 Entry


    Name = tk.StringVar()   # 建立文字變數
    Name.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='電腦User Name:',font=('Arial',20,'bold')).place(relx=0, rely=0.68)
    tk.Entry(User_UI, textvariable=Name).place(relx=0.33, rely=0.7)  # 放入 Entry

    Google_Data = tk.StringVar()   # 建立文字變數
    Google_Data.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='Google Profile Name:',font=('Arial',20,'bold')).place(relx=0, rely=0.75)
    OptionList = ['Default','Profile 2','Profile 3','Profile 4','Profile 5']   # 選項
    menu = tk.OptionMenu(User_UI, Google_Data, *OptionList).place(relx=0.42, rely=0.76)                # 第二個參數是取值，第三個開始是選項，使用星號展開

    tk.Label(User_UI, text='場次類型:',font=('Arial',20,'bold')).place(relx=0, rely=0.8)
    Session_List = ['單一場次','多場次']   # 選項
    Session_Value = tk.StringVar()  # 取值
    Session_Value.set('')
    Session_Menu = tk.OptionMenu(User_UI, Session_Value, *Session_List)                # 第二個參數是取值，第三個開始是選項，使用星號展開
    Session_Menu.place(relx=0.2, rely=0.8)  

    tk.Label(User_UI, text='愈搶的場次順序:',font=('Arial',20,'bold')).place(relx=0, rely=0.85)
    Session_SelectList = [1,2,3,4,5,6,7,8,9,10]   # 選項
    Session_Select = tk.StringVar()  # 取值
    Session_Select.set('')
    Session_Result = tk.OptionMenu(User_UI, Session_Select, *Session_SelectList)
    Session_Result.place(relx=0.32, rely=0.85)
    tk.Label(User_UI, text='*多場次才需要填寫此部分',font=('Arial',12,'bold')).place(relx=0, rely=0.9)
    
    Submit_Button = tk.Button(User_UI, text='送出', font=('Arial',20), width=5, command=lambda: Input_Checking() ).place(relx=0.4, rely=0.92)

    User_UI.mainloop()  # 放在主迴圈中