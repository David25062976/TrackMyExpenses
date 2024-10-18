import json
import os
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from datetime import datetime

from config import *
from data_access import *
from category_setting import category_setting
from show_records import show_records

def on_button_click():
    """齿轮按钮点击事件"""
    print("Button clicked!")

root.title( 'Take My Money' )        # 設定標題
root.iconbitmap( 'TME.ico' )  # 設定 icon
root.configure( background = bg_color )   # 設定背景色
root.resizable( True, True )   # 設定 x 方向和 y 方向的縮放

window_width = root.winfo_screenwidth()    # 取得螢幕寬度
window_height = root.winfo_screenheight()  # 取得螢幕高度

width = 1200
height = 800
left = int( ( window_width - width ) / 2 )       # 計算左上 x 座標
top = int( ( window_height - height ) / 2 )      # 計算左上 y 座標
root.geometry( f'{width}x{height}+{left}+{top}' )

main_tab.place( relx = 0, rely = 0, relwidth = 1, relheight = 1 )

# Home --------------------------------------------------------------------------------------------
main_tab.add( home_tab, text = 'Home' )

home_title_label = tk.Label(    # 標題 Take My Money
    home_tab,
    text = "Take My Money",
    font = ( 'Arial', 48,'bold' ),
    bg = bg_color,
    fg = '#000'
)
home_title_label.place( relx = 0.5, y = 150, anchor = 'center' )

def switch2() :
    main_tab.select( keep_accounts_tab )
keep_accounts_btn = tk.Button(
    home_tab,
    text = 'Keep Accounts',
    font = ( 'Arial',30,'bold' ),
    width = 17,
    height = 1,
    activeforeground = '#f00',
    command = switch2
)
keep_accounts_btn.place( relx = 0.5, y = 300, anchor = 'center' )

def switch3() :
    main_tab.select( recent_tab )
recent_btn = tk.Button(
    home_tab,
    text = '10 Recent Expenses',
    font = ( 'Arial',30,'bold' ),
    width = 17,
    height = 1,
    activeforeground = '#f00',
    command = switch3
)
recent_btn.place( relx = 0.5, y = 400, anchor = 'center' )

def switch4() :
    main_tab.select( expenses_search_tab )
expenditure_inquiry_btn = tk.Button(
    home_tab,
    text = 'Expenses Search',
    font = ( 'Arial',30,'bold' ),
    width = 17,
    height = 1,
    activeforeground = '#f00',
    command = switch4
)
expenditure_inquiry_btn.place( relx = 0.5, y = 500, anchor = 'center' )

# Keep Accounts -----------------------------------------------------------------------------------
main_tab.add( keep_accounts_tab,text = 'Keep Accounts' )

keep_accounts_title_label = tk.Label(    # 標題 Keep Accounts
    keep_accounts_tab,
    text = "Keep Accounts",
    font = ( 'Arial', 48,'bold' ),
    bg = bg_color,
    fg = '#000'
)
keep_accounts_title_label.place( relx = 0.5, y = 150, anchor = 'center' )

date_title_label = tk.Label(    # Date 的文字
    keep_accounts_tab,
    text = "Date",
    font = ( 'Arial', 24,'bold' ),
    bg = bg_color,
    fg = '#000'
)
date_title_label.place( relx = 0.5, x = -450, y = 210, anchor = 'w' )

year_label = tk.Label(    # 年份的文字
    keep_accounts_tab,
    text = "year",
    font = ( 'Arial', 16,'bold' ),
    bg = bg_color,
    fg = '#000'
)
year_label.place( relx = 0.5, x = -420, y = 250, anchor = 'center' )

def validate_year( P ) :    # 驗證年份輸入
    if P == "" :
        return True
    if P.isdigit() and int( P ) <= now.year :
        return True
    return False

year_spinbox = tk.Spinbox(    # 年份的spinbox
    keep_accounts_tab, 
    from_ = 0,   # 最小值
    to = now.year,    # 最大值
    width = 5,
    font = ( 'Arial', 20, 'bold' ),
    validate = 'key',  # 開啟輸入驗證
    validatecommand = ( root.register( validate_year ), '%P' ),  # 驗證函數
    increment = 1,  # 增量步長
)
year_spinbox.place( relx = 0.5, x = -340, y = 250, anchor = 'center' )
year_spinbox.delete( 0, tk.END )  # 清除當前内容
year_spinbox.insert( 0, now.year )  # 插入當前年份作為初始值

month_label = tk.Label(    # 月份的文字
    keep_accounts_tab,
    text = "month",
    font = ( 'Arial', 16,'bold' ),
    bg = bg_color,
    fg = '#000'
)
month_label.place( relx = 0.5, x = -240, y = 250, anchor = 'center' )

def validate_month( P ) :    # 驗證月份輸入
    if P == "" :
        return True
    if P.isdigit() and int( P ) >= 1 and int( P ) <= 12 :
        return True
    return False

month_spinbox = tk.Spinbox(
    keep_accounts_tab, 
    from_ = 1,   # 最小值
    to = 12,    # 最大值
    width = 5,
    font = ( 'Arial', 20, 'bold' ),
    wrap = True,
    validate = 'key',  # 開啟輸入驗證
    validatecommand = ( root.register( validate_month ), '%P' ),  # 驗證函數
    increment = 1,  # 增量步長
)
month_spinbox.place( relx = 0.5, x = -150, y = 250, anchor = 'center' )
month_spinbox.delete( 0, tk.END )  # 清除當前内容
month_spinbox.insert( 0, now.month )  # 插入當前月份作為初始值

day_label = tk.Label(    # 日期的文字
    keep_accounts_tab,
    text = "day",
    font = ( 'Arial', 16,'bold' ),
    bg = bg_color,
    fg = '#000'
)
day_label.place( relx = 0.5, x = -60, y = 250, anchor = 'center' )

big_month = [ 1, 3, 5, 7, 8, 10, 12 ]

def validate_day( P ) :    # 驗證日期輸入
    if P == "" :
        return True
    elif int( month_spinbox.get() ) == 2 and int( P ) == 30 :
        return False
    elif int( month_spinbox.get() ) not in big_month and int( P ) == 31 :
        return False
    elif P.isdigit() and int( P ) >= 1 and int( P ) <= 31 :
        return True
    return False

def update_day_spinbox_max( *args ) :    # 根據月份來調整日期上限
    try :
        month = int( month_spinbox.get() )
        day_spinbox.config( to = 29 if month == 2 else ( 31 if month in big_month else 30 ) )
    except ValueError :
        pass  # 如果输入的不是整數，则忽略

day_spinbox = tk.Spinbox(
    keep_accounts_tab,
    from_ = 1,   # 最小值
    to = 29 if now.month == 2 else ( 31 if now in big_month else 30 ),    # 最大值
    width = 5,
    font = ( 'Arial', 20, 'bold' ),
    wrap = True,
    validate = 'key',  # 開啟輸入驗證
    validatecommand = ( root.register( validate_day ), '%P' ),  # 驗證函數
    increment = 1,  # 增量步長
)
day_spinbox.place( relx = 0.5, x = 20, y = 250, anchor = 'center' )
day_spinbox.delete( 0, tk.END )  # 清除當前内容
day_spinbox.insert( 0, now.day )  # 插入當前日期作為初始值

month_spinbox_var = tk.StringVar( value = now.month )    # 處理2月只有29天
month_spinbox.config( textvariable = month_spinbox_var )
month_spinbox_var.trace_add( "write", update_day_spinbox_max )

hour_label = tk.Label(    # 小時的文字
    keep_accounts_tab,
    text = "hour",
    font = ( 'Arial', 16,'bold' ),
    bg = bg_color,
    fg = '#000'
)
hour_label.place( relx = 0.5, x = 110, y = 250, anchor = 'center' )

def validate_hour( P ) :    # 驗證小時輸入
    if P == "" :
        return True
    if P.isdigit() and int( P ) >= 0 and int( P ) <= 23 :
        return True
    return False

hour_spinbox = tk.Spinbox(
    keep_accounts_tab, 
    from_ = 0,   # 最小值
    to = 23,    # 最大值
    width = 5,
    font = ( 'Arial', 20, 'bold' ),
    wrap = True,
    validate = 'key',  # 開啟輸入驗證
    validatecommand = ( root.register( validate_hour ), '%P' ),  # 驗證函數
    increment = 1,  # 增量步長
)
hour_spinbox.place( relx = 0.5, x = 190, y = 250, anchor = 'center' )
hour_spinbox.delete( 0, tk.END )  # 清除當前内容
hour_spinbox.insert( 0, now.hour )  # 插入當前小時作為初始值

minute_label = tk.Label(    # 分鐘的文字
    keep_accounts_tab,
    text = "minute",
    font = ( 'Arial', 16,'bold' ),
    bg = bg_color,
    fg = '#000'
)
minute_label.place( relx = 0.5, x = 300, y = 250, anchor = 'center' )

def validate_minute( P ) :    # 驗證分鐘輸入
    if P == "" :
        return True
    if P.isdigit() and int( P ) >= 0 and int( P ) <= 59 :
        return True
    return False

minute_spinbox = tk.Spinbox(
    keep_accounts_tab, 
    from_ = 0,   # 最小值
    to = 59,    # 最大值
    width = 5,
    font = ( 'Arial', 20, 'bold' ),
    wrap = True,
    validate = 'key',  # 開啟輸入驗證
    validatecommand = ( root.register( validate_minute ), '%P' ),  # 驗證函數
    increment = 1,  # 增量步長
)
minute_spinbox.place( relx = 0.5, x = 390, y = 250, anchor = 'center' )
minute_spinbox.delete( 0, tk.END )  # 清除當前内容
minute_spinbox.insert( 0, now.minute )  # 插入當前分鐘作為初始值

item_name_title_label = tk.Label(    # Item Name 的文字
    keep_accounts_tab,
    text = "Item Name",
    font = ( 'Arial', 24,'bold' ),
    bg = bg_color,
    fg = '#000'
)
item_name_title_label.place( relx = 0.5, x = -450, y = 310, anchor = 'w' )

def on_entry_click( anEntry, aWatermark ) :
    """function that gets called whenever entry is clicked"""
    if anEntry.get() == aWatermark :
       anEntry.delete( 0, "end" ) # delete all the text in the entry
       anEntry.insert( 0, '' ) #Insert blank for user input
       anEntry.config( fg = 'black' )
def on_focusout( anEntry, aWatermark ) :
    if anEntry.get() == '' :
        anEntry.insert( 0, aWatermark )
        anEntry.config( fg = 'grey' )

item_name_watermark = 'Pizza'
item_name_entry = tk.Entry(
    keep_accounts_tab,
    width = 20,
    font = ( 'Arial', 20,'bold' ),
    fg = 'grey'
)
item_name_entry.insert( 0, item_name_watermark )
item_name_entry.bind( '<FocusIn>', lambda event : on_entry_click( item_name_entry, item_name_watermark ) )
item_name_entry.bind( '<FocusOut>', lambda event : on_focusout( item_name_entry, item_name_watermark ) )
item_name_entry.place( relx = 0.5, x = -440, y = 355, anchor = 'w' )

category_title_label = tk.Label(    # Category 的文字
    keep_accounts_tab,
    text = "Category",
    font = ( 'Arial', 24,'bold' ),
    bg = bg_color,
    fg = '#000'
)
category_title_label.place( relx = 0.5, x = -450, y = 410, anchor = 'w' )

category_menu = ttk.Combobox( keep_accounts_tab, state='readonly', values = load_categories() )
category_menu.config(
    width = 20,
    font = ( 'Arial', 20,'bold' ),
)
category_menu.place( relx = 0.5, x = -440, y = 455, anchor = 'w' )
if not len( load_categories() ) == 0 :
    category_menu.current( 0 )

more_image = Image.open("more.png")  # 打开图标图像
more_image = more_image.resize( ( 30, 30 ) , Image.Resampling.LANCZOS )  # 调整大小至30x30像素
more_icon = ImageTk.PhotoImage( more_image )   # 将图像转换为Tkinter可以使用的格式

# 创建带有图标的按钮
more_button = tk.Button(
    keep_accounts_tab,
    image = more_icon,
    command = lambda : category_setting( root, category_menu ),
    bd = 0,
    bg = bg_color
)
more_button.place( relx = 0.5, x = -110, y = 455, anchor = 'w' )

price_title_label = tk.Label(    # Price 的文字
    keep_accounts_tab,
    text = "Price",
    font = ( 'Arial', 24,'bold' ),
    bg = bg_color,
    fg = '#000'
)
price_title_label.place( relx = 0.5, x = -450, y = 510, anchor = 'w' )

def validate_integer_input( char ) :
    """ 验证输入字符是否为整数 """
    return char.isdigit() or char == ""

price_watermark = '100'
price_entry = tk.Entry(
    keep_accounts_tab,
    width = 20,
    font = ( 'Arial', 20,'bold' ),
    validate = "key" ,
    validatecommand = ( keep_accounts_tab.register( validate_integer_input ), "%S" ),
    fg = 'grey'
)
price_entry.insert( 0, price_watermark )
price_entry.bind( '<FocusIn>', lambda event : on_entry_click( price_entry, price_watermark ) )
price_entry.bind( '<FocusOut>', lambda event : on_focusout( price_entry, price_watermark ) )
price_entry.place( relx = 0.5, x = -440, y = 555, anchor = 'w' )

check_image = Image.open("check.png")  # 打开图标图像
check_image = check_image.resize( ( 250, 250 ) , Image.Resampling.LANCZOS )  # 調整大小
check_icon = ImageTk.PhotoImage( check_image )   # 将图像转换为Tkinter可以使用的格式

def ui_add_record() :
    fYear = year_spinbox.get().zfill( 4 )    # 補0到4位數
    fMonth = month_spinbox.get().zfill( 2 )    # 補0到2位數
    fDay = day_spinbox.get().zfill( 2 )    # 補0到2位數
    fHour = hour_spinbox.get().zfill( 2 )    # 補0到2位數
    fMinute = minute_spinbox.get().zfill( 2 )    # 補0到2位數

    date = f"{fYear}-{fMonth}-{fDay}-{fHour}-{fMinute}"
    item_name = item_name_entry.get()
    category = category_menu.get()
    price = int( price_entry.get() )

    record = { "date" : date, "item_name" : item_name, "category" : category, "price" : price }
    print( "add record :", record )
    add_record( record )

check_button = tk.Button(
    keep_accounts_tab,
    image = check_icon,
    command = ui_add_record,
    bd = 0,
    bg = bg_color
)
check_button.place( relx = 0.5, x = 50, y = 330, anchor = 'nw' )

# 10 Recent Expenses ------------------------------------------------------------------------------
main_tab.add( recent_tab, text='Recent Expenses' )

show_records()

# Expenses Search ---------------------------------------------------------------------------------
expenses_search_tab.place(x=100,y=30)
main_tab.add(expenses_search_tab, text='Expenses Search')

root.mainloop()