import tkinter as tk

root = tk.Tk()
root.geometry("300x200")

# 创建一些其他的元素
for i in range(5):
    tk.Label(root, text=f"Item {i + 1}").grid(row=i, column=0, padx=10, pady=5)

# 配置行和列的权重，确保所有元素可以自动扩展
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)  # 添加一个额外的行来保持 Label 在底部

# 创建固定在底部的 Label
bottom_label = tk.Label(root, text="This label is at the bottom", bg="lightgrey")
bottom_label.grid(row=6, column=0, sticky="s", padx=10, pady=5)  # `sticky="s"` 确保 Label 固定在底部

# 确保最后一行的高度足够显示底部的 Label
root.grid_rowconfigure(6, weight=0)

root.mainloop()
