import tkinter as tk
from selenium import webdriver
from Train_Ticket import service
from Train_Ticket import Train_Ticket_Prepare
from Train_Ticket import Train_Ticket_Confirm
from Train_Ticket import Train_Ticket_Payment
import time
import datetime
from tkinter import messagebox

def launch_selenium():
    User_Id=Id.get()
    User_StartStation = StartStation_Value.get()
    User_TargetStation = TargetStation_Value.get()
    Target_Date = Date.get()
    User_TrainNumber = TrainNumber.get()
    
    
    print('User_Id:',User_Id)
    print('User_StartStation:',User_StartStation)
    print('User_TargetStation:',User_TargetStation)
    print('User_TrainNumber:',User_TrainNumber)
    print('Target_Date:',Target_Date)

    driver = webdriver.Chrome(service=service)
    url = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query"
    Train_Ticket_Prepare(driver,url,User_StartStation,User_TargetStation,User_Id,User_TrainNumber,Target_Date)
    Train_Ticket_Confirm(driver)
    Train_Ticket_Payment(driver)

    time.sleep(30)
    return


def Reservation_Checking():
    Reservation = Reservation_Mode.get()
    print('Reservation:',Reservation)

    if Reservation=="True":
        print('Reservation Mode is ON...')
        Today = datetime.datetime.now()
        Tomorrow = Today + datetime.timedelta(days=1)

        if Year.get() == "":
            Reserve_Year = Tomorrow.year
            print('Default Year:',Reserve_Year)
        else:
            Reserve_Year = int(Year.get())
            print('Year:',Reserve_Year)

        if Month.get() == "":
            Reserve_Month = Tomorrow.month
            print('Default Month:',Reserve_Month)
        else:
            Reserve_Month = int(Month.get())
            print('Month:',Reserve_Month)

        if Day.get() == "":
            Reserve_Day = Tomorrow.day
            print('Default Day:',Reserve_Day)
        else:
            Reserve_Day = int(Day.get())
            print('Day:',Reserve_Day)

        if Hour.get() == "":
            Reserve_Hour = 0
            print('Default Hour:',Reserve_Hour)
        else:
            Reserve_Hour = int(Hour.get())
            print('Hour:',Reserve_Hour)

        if Min.get() == "":
            Reserve_Min =  0
            print('Default Minute:',Reserve_Min)
        else:
            Reserve_Min = int(Min.get())
            print('Minute:',Reserve_Min)

        startTime = datetime.datetime(Reserve_Year, Reserve_Month, Reserve_Day, Reserve_Hour, Reserve_Min, 0)
        while datetime.datetime.now() < startTime:
            time.sleep(1)
        print('Program now starts on %s' % startTime)
        print('Executing...')
        launch_selenium()

    else:
        print('Reservation Mode is OFF.')
        launch_selenium()
    
    return

def Input_Checking():
    User_Id=Id.get()
    User_StartStation = StartStation_Value.get()
    User_TargetStation = TargetStation_Value.get()
    Target_Date = Date.get()
    User_TrainNumber = TrainNumber.get()

    Input_List = [len(User_Id), len(User_StartStation), len(User_TargetStation), len(Target_Date), len(User_TrainNumber)]

    Check_Result=index_withoutexception(Input_List,0)


    if  Check_Result == -1:
        Reservation_Checking()
    else:
        messagebox.showinfo('showinfo', '基本資料有少，請重新輸入')

    return


def index_withoutexception(self,i):
    try:
        return self.index(i)
    except:
        return -1


if __name__ == '__main__':
    User_UI = tk.Tk()   # 建立 tkinter 視窗物件
    User_UI.title('火車自動訂票程式') # 設定標題
    width = 700
    height = 600
    left = 0
    top = 0
    User_UI.geometry(f'{width}x{height}+{left}+{top}')  # 定義視窗的尺寸和位置

    tk.Label(User_UI, text='身分證字號',font=('Arial',20,'bold')).grid(column=0, row=0)
    Id = tk.StringVar()   # 建立文字變數
    Id.set('')            # 一開始設定沒有內容
    tk.Entry(User_UI, textvariable=Id).grid(column=1, row=0)  # 放入 Entry
    tk.Label(User_UI, text='輸入格式範例:A123456789',font=('Arial',12,'bold')).grid(column=2, row=0)
    
    Station_Label = tk.Label(User_UI, text='起程站',font=('Arial',20,'bold')).grid(column=0, row=1)
    Station_List = ['5230-知本','3300-臺中']   # 選項
    StartStation_Value = tk.StringVar()                                        # 取值
    StartStation_Value.set('')
    StartStation_Menu = tk.OptionMenu(User_UI, StartStation_Value, *Station_List)                # 第二個參數是取值，第三個開始是選項，使用星號展開
    StartStation_Menu.grid(column=1, row=1)

    tk.Label(User_UI, text='到達站',font=('Arial',20,'bold')).grid(column=0, row=2)
    TargetStation_Value = tk.StringVar()                                        # 取值
    TargetStation_Value.set('')
    TargetStation_Menu = tk.OptionMenu(User_UI, TargetStation_Value, *Station_List)                # 第二個參數是取值，第三個開始是選項，使用星號展開
    TargetStation_Menu.grid(column=1, row=2)
    

    tk.Label(User_UI, text='欲搭乘日期',font=('Arial',20,'bold')).grid(column=0, row=3)
    Date= tk.StringVar()   # 建立文字變數
    Date.set('')            # 一開始設定沒有內容
    tk.Entry(User_UI, textvariable=Date).grid(column=1, row=3)  # 放入 Entry
    tk.Label(User_UI, text='輸入格式範例:20221028',font=('Arial',12,'bold')).grid(column=2, row=3)
    

    tk.Label(User_UI, text='欲搭乘車次',font=('Arial',20,'bold')).grid(column=0, row=4)
    TrainNumber= tk.StringVar()   # 建立文字變數
    TrainNumber.set('')            # 一開始設定沒有內容
    tk.Entry(User_UI, textvariable=TrainNumber).grid(column=1, row=4)  # 放入 Entry
    tk.Label(User_UI, text='輸入格式範例:110',font=('Arial',12,'bold')).grid(column=2, row=4)
    
    tk.Label(User_UI, text='是否為預約模式?',font=('Arial',20,'bold')).grid(column=0, row=5)
    Reservation_Mode = tk.StringVar()   # 設定文字變數
    radio_btn1 = tk.Radiobutton(User_UI, text='是', font=('Arial',20,'bold'), variable=Reservation_Mode, value='True').grid(column=1, row=5)
    radio_btn2 = tk.Radiobutton(User_UI, text='否', font=('Arial',20,'bold'), variable=Reservation_Mode, value='False').grid(column=2, row=5)

    tk.Label(User_UI, text='預約日期與時間設定',font=('Arial',20,'bold')).grid(column=0, row=6)
    tk.Label(User_UI, text='(預約模式才需填寫)',font=('Arial',12,'bold')).grid(column=1, row=6)

    
    Year = tk.StringVar()   # 建立文字變數
    Year.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='年',font=('Arial',20,'bold')).grid(column=1, row=7)
    tk.Entry(User_UI, textvariable=Year).grid(column=0, row=7)  # 放入 Entry

    Month = tk.StringVar()   # 建立文字變數
    Month.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='月',font=('Arial',20,'bold')).grid(column=1, row=8)
    tk.Entry(User_UI, textvariable=Month).grid(column=0, row=8)  # 放入 Entry

    Day = tk.StringVar()   # 建立文字變數
    Day.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='日',font=('Arial',20,'bold')).grid(column=1, row=9)
    tk.Entry(User_UI, textvariable=Day).grid(column=0, row=9)  # 放入 Entry

    Hour = tk.StringVar()   # 建立文字變數
    Hour.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='時',font=('Arial',20,'bold')).grid(column=1, row=10)
    tk.Entry(User_UI, textvariable=Hour).grid(column=0, row=10)  # 放入 Entry

    Min = tk.StringVar()   # 建立文字變數
    Min.set('')            # 一開始設定沒有內容
    tk.Label(User_UI, text='分',font=('Arial',20,'bold')).grid(column=1, row=11)
    tk.Entry(User_UI, textvariable=Min).grid(column=0, row=11)  # 放入 Entry


    Submit_Button = tk.Button(User_UI, text='送出', font=('Arial',20), width=5, command=lambda: Input_Checking() ).grid(column=1, row=12)

    

    User_UI.mainloop()  # 放在主迴圈中