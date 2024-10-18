import tkinter as tk
from PIL import Image, ImageTk

from category_setting import category_setting
from data_access import *
from config import *

page = 1
root = recent_tab
record_frame = tk.Frame( root, bg ='white' )
page_value = tk.IntVar()
page_value.set( page )
edit_buttons = []
delete_buttons = []

sort_by = "date"
sort_reverse = True

def next_page() :
    global page, sort_by, sort_reverse
    page += 1
    records = load_records()
    if ( page - 1 ) * 10 > len( records ) :
        page = 1
    
    page_value.set( page )
    update_show_records()

def previous_page() :
    global page, sort_by, sort_reverse
    page -= 1
    records = load_records()
    if page < 1 :
        page = int( len( records ) / 10 ) + 1
    
    page_value.set( page )
    update_show_records()

def sr_delete_record( index ) :
    delete_record( index )
    update_show_records()

def sr_edit_record( index ) :
    editing_window = tk.Toplevel( record_frame )
    editing_window.title( "Editing Record" )
    editing_window.geometry( "1200x800" )
    editing_window.configure( bg = bg_color )
    records = load_records()

    date_title_label = tk.Label(    # Date 的文字
        editing_window,
        text = "Date",
        font = ( 'Arial', 24,'bold' ),
        bg = bg_color,
        fg = '#000'
    )
    date_title_label.place( relx = 0.5, x = -450, y = 210, anchor = 'w' )

    year_label = tk.Label(    # 年份的文字
        editing_window,
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
        editing_window, 
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
    year_spinbox.insert( 0, records[ index ][ 'date' ][ 0 : 4 ] )  # 插入當前年份作為初始值

    month_label = tk.Label(    # 月份的文字
        editing_window,
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
        editing_window, 
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
    month_spinbox.insert( 0, records[ index ][ 'date' ][ 5 : 7 ] )  # 插入當前月份作為初始值

    day_label = tk.Label(    # 日期的文字
        editing_window,
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
        editing_window,
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
    day_spinbox.insert( 0, records[ index ][ 'date' ][ 8 : 10 ] )  # 插入當前日期作為初始值

    month_spinbox_var = tk.StringVar( value = now.month )    # 處理2月只有29天
    month_spinbox.config( textvariable = month_spinbox_var )
    month_spinbox_var.trace_add( "write", update_day_spinbox_max )

    hour_label = tk.Label(    # 小時的文字
        editing_window,
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
        editing_window, 
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
    hour_spinbox.insert( 0, records[ index ][ 'date' ][ 11 : 13 ] )  # 插入當前小時作為初始值

    minute_label = tk.Label(    # 分鐘的文字
        editing_window,
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
        editing_window, 
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
    minute_spinbox.insert( 0, records[ index ][ 'date' ][ 14 :  ] )  # 插入當前分鐘作為初始值

    item_name_title_label = tk.Label(    # Item Name 的文字
        editing_window,
        text = "Item Name",
        font = ( 'Arial', 24,'bold' ),
        bg = bg_color,
        fg = '#000'
    )
    item_name_title_label.place( relx = 0.5, x = -450, y = 310, anchor = 'w' )

    item_name_entry = tk.Entry(
        editing_window,
        width = 20,
        font = ( 'Arial', 20,'bold' ),
        fg = '#000'
    )
    item_name_entry.place( relx = 0.5, x = -440, y = 355, anchor = 'w' )
    item_name_entry.delete( 0, tk.END )
    item_name_entry.insert( 0, records[ index ][ 'item_name' ] )

    category_title_label = tk.Label(    # Category 的文字
        editing_window,
        text = "Category",
        font = ( 'Arial', 24,'bold' ),
        bg = bg_color,
        fg = '#000'
    )
    category_title_label.place( relx = 0.5, x = -450, y = 410, anchor = 'w' )

    category_menu = ttk.Combobox( editing_window, state='readonly', values = load_categories() )
    category_menu.config(
        width = 20,
        font = ( 'Arial', 20,'bold' ),
    )
    category_menu.place( relx = 0.5, x = -440, y = 455, anchor = 'w' )
    if records[ index ][ 'category' ] in load_categories() :
        category_menu.set( records[ index ][ 'category' ] )
    elif not len( load_categories() ) == 0 :
        category_menu.current( 0 )

    more_image = Image.open("imgs/more.png")  # 打开图标图像
    more_image = more_image.resize( ( 30, 30 ) , Image.Resampling.LANCZOS )  # 调整大小至30x30像素
    more_icon = ImageTk.PhotoImage( more_image )   # 将图像转换为Tkinter可以使用的格式

    # 创建带有图标的按钮
    more_button = tk.Button(
        editing_window,
        image = more_icon,
        command = lambda : category_setting( root, category_menu ),
        bd = 0,
        bg = bg_color
    )
    more_button.place( relx = 0.5, x = -110, y = 455, anchor = 'w' )
    editing_window.more_icon = more_icon

    price_title_label = tk.Label(    # Price 的文字
        editing_window,
        text = "Price",
        font = ( 'Arial', 24,'bold' ),
        bg = bg_color,
        fg = '#000'
    )
    price_title_label.place( relx = 0.5, x = -450, y = 510, anchor = 'w' )

    def validate_integer_input( char ) :
        """ 验证输入字符是否为整数 """
        return char.isdigit() or char == ""

    price_entry = tk.Entry(
        editing_window,
        width = 20,
        font = ( 'Arial', 20,'bold' ),
        validate = "key" ,
        validatecommand = ( keep_accounts_tab.register( validate_integer_input ), "%S" ),
        fg = '#000'
    )
    price_entry.place( relx = 0.5, x = -440, y = 555, anchor = 'w' )
    price_entry.delete( 0, tk.END )
    price_entry.insert( 0, records[ index ][ 'price' ] )

    check_image = Image.open("imgs/check.png")  # 打开图标图像
    check_image = check_image.resize( ( 250, 250 ) , Image.Resampling.LANCZOS )  # 調整大小
    check_icon = ImageTk.PhotoImage( check_image )   # 将图像转换为Tkinter可以使用的格式

    def sr_edit_record() :
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
        print( "edited record :", record )
        edit_record( index, record )
        update_show_records()
        editing_window.destroy()

    check_button = tk.Button(
        editing_window,
        image = check_icon,
        command = sr_edit_record,
        bd = 0,
        bg = bg_color
    )
    check_button.place( relx = 0.5, x = 50, y = 330, anchor = 'nw' )
    editing_window.check_icon = check_icon

def sort_by_date() :
    global sort_by, sort_reverse
    if sort_by == "date" :
        sort_reverse = not sort_reverse
    else :
        sort_by = "date"
        sort_reverse = True
    
    update_show_records()

def sort_by_category() :
    global sort_by, sort_reverse
    if sort_by == "category" :
        sort_reverse = not sort_reverse
    else :
        sort_by = "category"
        sort_reverse = False
    
    update_show_records()

def sort_by_price() :
    global sort_by, sort_reverse
    if sort_by == "price" :
        sort_reverse = not sort_reverse
    else :
        sort_by = "price"
        sort_reverse = True
    
    update_show_records()

def update_show_records() :
    for widget in record_frame.winfo_children():
        widget.destroy()

    records = load_records()
    records.sort( key = lambda x : x[ sort_by ], reverse = sort_reverse )

    date_label = tk.Button(
        record_frame,
        text = "Date",
        width = 14,
        font = ( 'Arial', 20,'bold' ),
        command = sort_by_date,
        bg = bg_color,
        fg = '#000',
        relief = 'solid',
        bd = 2
    )
    date_label.grid( row = 0, column = 0 )

    item_name_label = tk.Button(
        record_frame,
        text = "Item Name",
        width = 14,
        font = ( 'Arial', 20,'bold' ),
        bg = bg_color,
        fg = '#000',
        relief = 'solid',
        bd = 2
    )
    item_name_label.grid( row = 0, column = 1 )

    category_label = tk.Button(
        record_frame,
        text = "Category",
        width = 14,
        font = ( 'Arial', 20,'bold' ),
        command = sort_by_category,
        bg = bg_color,
        fg = '#000',
        relief = 'solid',
        bd = 2
    )
    category_label.grid( row = 0, column = 2 )

    price_label = tk.Button(
        record_frame,
        text = "price",
        width = 14,
        font = ( 'Arial', 20,'bold' ),
        command = sort_by_price,
        bg = bg_color,
        fg = '#000',
        relief = 'solid',
        bd = 2
    )
    price_label.grid( row = 0, column = 3 )

    empty_label = tk.Button(
        record_frame,
        width = 4,
        font = ( 'Arial', 20,'bold' ),
        bg = bg_color,
        fg = '#000',
        relief = 'solid',
        bd = 2
    )
    empty_label.grid( row = 0, column = 4, columnspan = 2 )

    delete_image = Image.open("imgs/bin.png")  # 打开图标图像
    delete_image = delete_image.resize( ( 30, 30 ) , Image.Resampling.LANCZOS )  # 调整大小至30x30像素
    delete_icon = ImageTk.PhotoImage( delete_image )   # 将图像转换为Tkinter可以使用的格式

    edit_image = Image.open("imgs/edit.png")  # 打开图标图像
    edit_image = edit_image.resize( ( 30, 30 ) , Image.Resampling.LANCZOS )  # 调整大小至30x30像素
    edit_icon = ImageTk.PhotoImage( edit_image )   # 将图像转换为Tkinter可以使用的格式

    if page * 10 > len( records ) :
        target_records = records[ ( page - 1 ) * 10 : len( records ) ]
    else :
        target_records = records[ ( page - 1 ) * 10 : ( page - 1 ) * 10 + 10 ]
    for i, record in enumerate( target_records ) :
        date = tk.Label(
            record_frame,
            text = record["date"],
            width = 14,
            font = ( 'Arial', 20,'bold' ),
            bg = 'white',
            fg = '#000',
        )
        date.grid( row = i + 1, column = 0 )

        item_name = tk.Label(
            record_frame,
            text = record["item_name"],
            width = 14,
            font = ( 'Arial', 20,'bold' ),
            bg = '#dcdcdc',
            fg = '#000',
        )
        item_name.grid( row = i + 1, column = 1 )

        category = tk.Label(
            record_frame,
            text = record["category"],
            width = 14,
            font = ( 'Arial', 20,'bold' ),
            bg = 'white',
            fg = '#000',
        )
        category.grid( row = i + 1, column = 2 )

        price = tk.Label(
            record_frame,
            text = record["price"],
            width = 14,
            font = ( 'Arial', 20,'bold' ),
            bg = '#dcdcdc',
            fg = '#000',
        )
        price.grid( row = i + 1, column = 3 )

        edit_button = tk.Button(
            record_frame,   
            image = edit_icon,
            width = 30,
            height = 30,
            command = lambda i = i : sr_edit_record( ( page - 1 ) * 10 + i ),
            bd = 0,
            bg = 'white'
        )
        edit_button.grid( row = i + 1, column = 4 )

        edit_buttons.append( edit_button )
        record_frame.edit_icon = edit_icon

        delete_button = tk.Button(
            record_frame,   
            image = delete_icon,
            width = 30,
            height = 30,
            command = lambda i = i : sr_delete_record( ( page - 1 ) * 10 + i ),
            bd = 0,
            bg = 'white'
        )
        delete_button.grid( row = i + 1, column = 5 )

        delete_buttons.append( delete_button )
        record_frame.delete_icon = delete_icon

    record_frame.place( relx = 0.5, y = 200, anchor = 'n' )

def update_ui() :
    recent_title_label = tk.Label(    # 標題 Keep Accounts
        root,
        text = "Recent Expenses",
        font = ( 'Arial', 48,'bold' ),
        bg = bg_color,
        fg = '#000'
    )
    recent_title_label.place( relx = 0.5, y = 150, anchor = 'center' )

    update_show_records()

    left_image = Image.open("imgs/left.png")  # 打开图标图像
    left_image = left_image.resize( ( 40, 40 ) , Image.Resampling.LANCZOS )  # 调整大小至30x30像素
    left_icon = ImageTk.PhotoImage( left_image )   # 将图像转换为Tkinter可以使用的格式

    left_button = tk.Button(
        root,
        image = left_icon,
        bg = bg_color,
        command = previous_page,
        bd = 0,
    )
    left_button.place( relx = 0.5, x = -150, y = 700, anchor = 'center' )
    root.left_icon = left_icon

    right_image = Image.open("imgs/right.png")  # 打开图标图像
    right_image = right_image.resize( ( 40, 40 ) , Image.Resampling.LANCZOS )  # 调整大小至30x30像素
    right_icon = ImageTk.PhotoImage( right_image )   # 将图像转换为Tkinter可以使用的格式

    right_button = tk.Button(
        root,
        image = right_icon,
        bg = bg_color,
        command = next_page,
        bd = 0,
    )
    right_button.place( relx = 0.5, x = 150, y = 700, anchor = 'center' )
    root.right_icon = right_icon

    page_number_label = tk.Label(
        root,
        textvariable = page_value,
        width = 4,
        font = ( 'Arial', 32,'bold' ),
        bg = 'white',
        fg = '#000',
        relief = 'solid'
    )
    page_number_label.place( relx = 0.5, y = 700, anchor = 'center' )

def show_records() :
    update_ui()