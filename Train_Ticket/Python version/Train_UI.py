import tkinter as tk
from selenium import webdriver
from Train_Ticket import service
from Train_Ticket import Train_Ticket_Prepare
from Train_Ticket import Train_Ticket_Confirm
from Train_Ticket import Train_Ticket_Payment
import time

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

if __name__ == '__main__':
    User_UI = tk.Tk()   # 建立 tkinter 視窗物件
    User_UI.title('火車自動訂票程式') # 設定標題
    width = 600
    height = 400
    left = 0
    top = 0
    User_UI.geometry(f'{width}x{height}+{left}+{top}')  # 定義視窗的尺寸和位置

    tk.Label(User_UI, text='身分證字號',font=('Arial',20,'bold')).grid(column=0, row=0)
    Id = tk.StringVar()   # 建立文字變數
    Id.set('')            # 一開始設定沒有內容
    tk.Entry(User_UI, textvariable=Id).grid(column=1, row=0)  # 放入 Entry
    tk.Label(User_UI, text='輸入格式範例:A123456789').grid(column=2, row=0)
    
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
    tk.Label(User_UI, text='輸入格式範例:20221028').grid(column=2, row=3)
    

    tk.Label(User_UI, text='欲搭乘車次',font=('Arial',20,'bold')).grid(column=0, row=4)
    TrainNumber= tk.StringVar()   # 建立文字變數
    TrainNumber.set('')            # 一開始設定沒有內容
    tk.Entry(User_UI, textvariable=TrainNumber).grid(column=1, row=4)  # 放入 Entry
    tk.Label(User_UI, text='輸入格式範例:110').grid(column=2, row=4)
    


    Submit_Button = tk.Button(User_UI, text='送出', font=('Arial',20), width=5, command=lambda: launch_selenium() ).grid(column=1, row=5)

    User_UI.mainloop()  # 放在主迴圈中