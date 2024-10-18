import tkinter as tk
from PIL import Image, ImageTk

from data_access import load_categories, save_categories
from config import *

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

def on_delete_click( index, root, category_menu ) :
    """按钮点击事件，删除 list a 中的对应元素并更新 UI"""
    if 0 <= index < len( category_list ) :
        del category_list[ index ]  # 删除 list a 中的对应元素
        save_categories( category_list )
        update_ui( root, category_menu )  # 更新界面

def on_add_click( str, root, category_menu ) :
    category_list.append( str )
    save_categories( category_list )
    update_ui( root, category_menu )  # 更新界面

category_list = load_categories()
labels = []
buttons = []
item_name_entry = None
gear_button = None

def update_ui( root, category_menu ) :
    global item_name_entry, gear_button  # 确保可以访问全局变量

    # 销毁现有的小部件
    for label in labels:
        label.destroy()
    for button in buttons:
        button.destroy()

    # 清空列表
    labels.clear()
    buttons.clear()

    try:
        if item_name_entry and item_name_entry.winfo_exists():
            item_name_entry.destroy()
    except NameError:
        pass  # 如果 item_name_entry 未定义，直接跳过

    try:
        if gear_button and gear_button.winfo_exists():
            gear_button.destroy()
    except NameError:
        pass  # 如果 gear_button 未定义，直接跳过

    bin_image = Image.open("bin.png")  # 打开图标图像
    bin_image = bin_image.resize( ( 40, 40 ) , Image.Resampling.LANCZOS )  # 调整大小至30x30像素
    bin_icon = ImageTk.PhotoImage( bin_image )   # 将图像转换为Tkinter可以使用的格式
    grey = False
    i = 0
    for i in range( len( labels ), len( category_list ) ) :
        category_label = tk.Label(    # Item Name 的文字
            root,
            text = category_list[i],
            width = 15,
            height = 1,
            font = ( 'Arial', 24,'bold' ),
            bg = '#dcdcdc' if grey else 'white',
            fg = '#000'
        )
        category_label.grid( column = 0, row = i )
        
        bin_button = tk.Button(
            root,
            image = bin_icon,
            width = 41,
            height = 41,
            command = lambda index = len( labels ) : on_delete_click( index, root, category_menu ),
            bd = 0,
            bg = 'white' if grey else '#dcdcdc'
        )
        bin_button.grid( column = 1, row = i )

        labels.append( category_label )
        buttons.append( bin_button )
        grey = not grey
    
        root.bin_icon = bin_icon

    item_name_watermark = 'new category'
    item_name_entry = tk.Entry(
        root,
        width = 16,
        font = ( 'Arial', 24,'bold' ),
        fg = 'grey',
        bg = '#dcdcdc' if grey else 'white',
    )
    item_name_entry.insert( 0, item_name_watermark )
    item_name_entry.bind( '<FocusIn>', lambda event : on_entry_click( item_name_entry, item_name_watermark ) )
    item_name_entry.bind( '<FocusOut>', lambda event : on_focusout( item_name_entry, item_name_watermark ) )
    item_name_entry.grid( column = 0, row = i + 1 )

    add_image = Image.open("more.png")  # 打开图标图像
    add_image = add_image.resize( ( 30, 30 ) , Image.Resampling.LANCZOS )  # 调整大小至30x30像素
    add_icon = ImageTk.PhotoImage( add_image )   # 将图像转换为Tkinter可以使用的格式

    gear_button = tk.Button(
        root,
        image = add_icon,
        width = 41,
        height = 41,
        command = lambda : on_add_click( item_name_entry.get(), root, category_menu ),
        bd = 0,
        bg = 'white' if grey else '#dcdcdc'
    )
    gear_button.grid( column = 1, row = i + 1 )

    root.add_icon = add_icon

    category_menu['values'] = category_list
    try :
        if category_menu.get() not in category_list :
            category_menu.current( 0 )
    except :
        pass

def category_setting( root, category_menu ) :
    setting_window = tk.Toplevel( root, bg = 'white' )
    setting_window.title( "category setting" )
    setting_window.resizable( False, False )

    update_ui( setting_window, category_menu )