import tkinter as tk
from selenium import webdriver
import time
import datetime
from tkinter import messagebox
from selenium.webdriver.chrome.service import Service
from KKTix_ticket import Login_Prepare,Target_Activity,Target_Order,Fulfill_Sheet,Ticket_Pament,Retry_Detect

def Main_KKTix_ticket(Reserve_Year, Reserve_Month, Reserve_Day, Reserve_Hour, Reserve_Min,User_Ticket_Count,Section_Order,Target_Price,Name,Password,Id):
    binary_path="C:\selenium_driver_chrome\chromedriver.exe"
    service=Service(binary_path)

    driver = webdriver.Chrome(service=service)
    Login_url = "https://kktix.com/users/sign_in?back_to=https%3A%2F%2Fkktix.com%2F"
    Login_Prepare(driver,Login_url,Name,Password) # 買票準備(登入) - Step 0.0

    Target_url = url.get()
    Target_Activity(driver,Target_url,Section_Order)  # 欲搶的活動  - Step 0.1

    startTime = datetime.datetime(Reserve_Year, Reserve_Month, Reserve_Day, Reserve_Hour, Reserve_Min, 0)
    while datetime.datetime.now() < startTime:
        time.sleep(1)
    print('Program now starts on %s' % startTime)
    print('Executing...')
    driver.refresh()
    time.sleep(0.5)

    Question_Page_url=Target_Order(driver,Target_Price,User_Ticket_Count) # 選擇票種和張數 - Step1
    # 劃位 - Step2 *若為電腦配位，這頁會跳過*
    # Seat_Selection(driver)
    # 填寫表單 - Step3
    Fulfill_Sheet(driver)
    # 取票繳費 - Step4
    Ticket_Pament(driver,Question_Page_url,Target_url,Id,Section_Order,Target_Price,User_Ticket_Count)
    print('成功搶到票，程式進入休眠....')
    time.sleep(6000)


    return

def Reservation_Checking():
    
    User_Session=Session_Value.get()
    print('User_Session:',User_Session)
    User_SelectSession=Session_Select.get()
    print('User_SelectSession:',User_SelectSession)

    if  User_Session == "單一場次":
        Section_Order='/html/body/div[2]/div[2]/div/div[8]/a'
        print('Section_Order:',Section_Order)
    else:
        Section_Order= '/html/body/div[2]/div/div[2]/div[2]/ul/li[' + User_SelectSession + ']/div/a'
        print('Section_Order:',Section_Order)


    Target_Price = Target_Price1.get()
    print('目標價格編號:',Target_Price)

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

    Input_List = [len(Month.get()),len(Day.get()),len(Hour.get()),len(Ticket_Count.get()),len(Target_Price)]
    Check_Result=index_withoutexception(Input_List,0)

    
    if  len(Month.get()) == 0 | len(Day.get()) ==0 :
        messagebox.showinfo('showinfo', '請輸入幾月幾號開搶')
    
    if  len(Hour.get()) ==0 :
        messagebox.showinfo('showinfo', '請輸入幾點開搶')

    if  len(Ticket_Count.get()) ==0 :
        messagebox.showinfo('showinfo', '請輸入搶票張數')

    if  len(Target_Price) == 0:
        messagebox.showinfo('showinfo', '請輸入目標價格編號')

    if  Check_Result == -1:
        Reserve_Month = int(Month.get())
        print('Month:',Reserve_Month)

        Reserve_Day = int(Day.get())
        print('Day:',Reserve_Day)

        Reserve_Hour = int(Hour.get())
        print('Hour:',Reserve_Hour)

    User_Ticket_Count=Ticket_Count.get()

    if  int(User_Ticket_Count) < 5:
        print('欲搶張數:',User_Ticket_Count)
        Name=User_Name.get()
        Password=User_Password.get()
        Id=User_Id.get()
        Main_KKTix_ticket(Reserve_Year, Reserve_Month, Reserve_Day, Reserve_Hour, Reserve_Min,User_Ticket_Count,Section_Order,Target_Price,Name,Password,Id)
    else:
        messagebox.showinfo('showinfo', '票數不可以超過4張')
    
    return

def Input_Checking():
    User_url=url.get()
    Name=User_Name.get()
    Password=User_Password.get()
    Id=User_Id.get()
    print('KKTix帳號:',Name)
    print('KKTix密碼:',Password)
    print('使用者身分證字號:',Id)

    Input_List = [len(User_url),len(Name),len(Password),len(Id)]

    Check_Result=index_withoutexception(Input_List,0)
    
    if  len(User_url) == 0:
        messagebox.showinfo('showinfo', '請輸入目標網址')

    if  len(Name) == 0:
        messagebox.showinfo('showinfo', '請輸入KKTix帳號')
    
    if  len(Password) == 0:
        messagebox.showinfo('showinfo', '請輸入KKTix密碼')

    if  len(Id) == 0:
        messagebox.showinfo('showinfo', '請輸入你的身分證字號')

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

     # 搶票網址
    tk.Label(User_UI, text='欲搶票的活動網址:',font=('Arial',20,'bold')).place(relx=0, rely=0)
    url = tk.StringVar() 
    url.set('')
    tk.Entry(User_UI, textvariable=url,width=50).place(relx=0.35, rely=0.015)  # 放入 Entry
    tk.Label(User_UI, text='輸入範例:https://nicemedia.kktix.cc/events/time-leap1st',font=('Arial',12,'bold')).place(relx=0.35, rely=0.055)

    # 預約日期與時間設定
    tk.Label(User_UI, text='預約日期與時間設定:',font=('Arial',20,'bold')).place(relx=0, rely=0.1)
    # 年
    Year = tk.StringVar() 
    Year.set('')
    tk.Label(User_UI, text='年',font=('Arial',20,'bold')).place(relx=0.18, rely=0.2)
    tk.Entry(User_UI, textvariable=Year,width=6).place(relx=0.1, rely=0.215)  # 放入 Entry
    tk.Label(User_UI, text='*預設為今年',font=('Arial',12,'bold')).place(relx=0.08, rely=0.26)
    # 月
    Month = tk.StringVar() 
    Month.set('')
    tk.Label(User_UI, text='月',font=('Arial',20,'bold')).place(relx=0.33, rely=0.2)
    tk.Entry(User_UI, textvariable=Month,width=6).place(relx=0.25, rely=0.215)  # 放入 Entry
    # 日
    Day = tk.StringVar() 
    Day.set('')
    tk.Label(User_UI, text='日',font=('Arial',20,'bold')).place(relx=0.48, rely=0.2)
    tk.Entry(User_UI, textvariable=Day,width=6).place(relx=0.4, rely=0.215)  # 放入 Entry
    # 小時
    Hour = tk.StringVar() 
    Hour.set('')
    tk.Label(User_UI, text='時',font=('Arial',20,'bold')).place(relx=0.63, rely=0.2)
    tk.Entry(User_UI, textvariable=Hour,width=6).place(relx=0.55, rely=0.215)  # 放入 Entry
    tk.Label(User_UI, text='*24小時制',font=('Arial',12,'bold')).place(relx=0.53, rely=0.27)
    # 分
    Min = tk.StringVar() 
    Min.set('')
    tk.Label(User_UI, text='分',font=('Arial',20,'bold')).place(relx=0.78, rely=0.2)
    tk.Entry(User_UI, textvariable=Min,width=6).place(relx=0.7, rely=0.215)  # 放入 Entry
    tk.Label(User_UI, text='*預設為0',font=('Arial',12,'bold')).place(relx=0.68, rely=0.27)
    # 秒
    Sec = tk.StringVar() 
    Sec.set('')
    tk.Label(User_UI, text='秒',font=('Arial',20,'bold')).place(relx=0.93, rely=0.2)
    tk.Entry(User_UI, textvariable=Sec,width=6).place(relx=0.85, rely=0.215)  # 放入 Entry
    tk.Label(User_UI, text='*預設為0',font=('Arial',12,'bold')).place(relx=0.83, rely=0.27)


    # 欲購買張數
    Ticket_Count = tk.StringVar() 
    Ticket_Count.set('')
    tk.Label(User_UI, text='欲購買張數:',font=('Arial',20,'bold')).place(relx=0, rely=0.3)
    tk.Entry(User_UI, textvariable=Ticket_Count,width=6).place(relx=0.25, rely=0.31)  # 放入 Entry

    # 目標價格編號
    Target_Price1 = tk.StringVar() 
    Target_Price1.set('')
    tk.Label(User_UI, text='目標價格編號:',font=('Arial',20,'bold')).place(relx=0, rely=0.35)
    tk.Entry(User_UI, textvariable=Target_Price1,width=6).place(relx=0.3, rely=0.36)  # 放入 Entry

    # KKTix帳號
    User_Name = tk.StringVar()
    User_Name.set('')
    tk.Label(User_UI, text='KKTix帳號:',font=('Arial',20,'bold')).place(relx=0, rely=0.4)
    tk.Entry(User_UI, textvariable=User_Name,width=30).place(relx=0.23, rely=0.41)  # 放入 Entry

    # KKTix密碼
    User_Password = tk.StringVar()
    User_Password.set('')
    tk.Label(User_UI, text='KKTix密碼:',font=('Arial',20,'bold')).place(relx=0, rely=0.45)
    tk.Entry(User_UI, textvariable=User_Password,width=30).place(relx=0.23, rely=0.46)  # 放入 Entry

    # 使用者身分證字號
    User_Id = tk.StringVar()
    User_Id.set('')
    tk.Label(User_UI, text='使用者身分證字號:',font=('Arial',20,'bold')).place(relx=0, rely=0.5)
    tk.Entry(User_UI, textvariable=User_Id).place(relx=0.36, rely=0.51)  # 放入 Entry

    # 場次類型
    tk.Label(User_UI, text='場次類型:',font=('Arial',20,'bold')).place(relx=0, rely=0.55)
    Session_List = ['單一場次','多場次']   # 選項
    Session_Value = tk.StringVar()  # 取值
    Session_Value.set('')
    Session_Menu = tk.OptionMenu(User_UI, Session_Value, *Session_List)                # 第二個參數是取值，第三個開始是選項，使用星號展開
    Session_Menu.place(relx=0.2, rely=0.55)  

    # 愈搶的場次順序
    tk.Label(User_UI, text='愈搶的場次順序:',font=('Arial',20,'bold')).place(relx=0, rely=0.6)
    Session_SelectList = [1,2,3,4,5,6,7,8,9,10]   # 選項
    Session_Select = tk.StringVar()  # 取值
    Session_Select.set('')
    Session_Result = tk.OptionMenu(User_UI, Session_Select, *Session_SelectList)
    Session_Result.place(relx=0.32, rely=0.6)
    tk.Label(User_UI, text='*多場次才需要填寫此部分',font=('Arial',12,'bold')).place(relx=0, rely=0.65)
    
    # 送出按鈕
    Submit_Button = tk.Button(User_UI, text='送出', font=('Arial',20), width=5, command=lambda: Input_Checking() ).place(relx=0.4, rely=0.7)

    User_UI.mainloop()  # 放在主迴圈中