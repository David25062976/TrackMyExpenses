import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime

root = tk.Tk()
FILE_PATH = "records.json"    # 文件路徑
bg_color = '#FFE4E1'
now = datetime.now()

main_tab = ttk.Notebook()
home_tab = tk.Frame( main_tab, bg = bg_color )
keep_accounts_tab=tk.Frame( main_tab, bg = bg_color )
recent_tab = tk.Frame( main_tab, bg = bg_color )
expenses_search_tab=tk.Frame(main_tab, bg = bg_color)