import tkinter as tk

root = tk.Tk()

# 共同的样式设置
common_style = {
    "font": ("Arial", 24, "bold"),
    "bg": "#f0f0f0",  # 背景颜色
    "fg": "black",    # 前景文字颜色
    "bd": 2,          # 边框宽度
    "relief": "raised"  # 边框样式，类似按钮的样式
}

# 创建 Label，使用 pady 来控制高度
label = tk.Label(root, text="Label", **common_style)
label.pack(padx=20, pady=20)

# 创建 Button，通过 `height` 设置具体像素高度来匹配 Label
button = tk.Button(root, text="Button", **common_style, height=1)
button.pack(padx=20, pady=20)

root.mainloop()
