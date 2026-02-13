import tkinter as tk
from tkinter import messagebox
import time

def countdown(seconds, label, root):
    if seconds >= 0:
        label.config(text='坚持住！距离胜利还有' + time.strftime("%H:%M:%S", time.gmtime(seconds)))
        # label.config(text=f"{seconds}")
        seconds -= 1
        label.after(1000, countdown, seconds, label, root)  # 1000毫秒即1秒后再次调用countdown函数
    else:
        root.withdraw()  # 隐藏倒计时窗口
        root.after(100, lambda: show_celebration(root))  # 100毫秒后显示庆祝消息框

def show_celebration(root):
    messagebox.showinfo("下班啦~ 回家咯~~~！！！")
    root.destroy()  # 关闭程序

if __name__ == '__main__':
    current_time = time.localtime()
    remaining_seconds = 18 * 3600 + 30 * 60 - (current_time.tm_hour * 3600 + current_time.tm_min * 60 + current_time.tm_sec)

    root = tk.Tk()
    root.attributes("-topmost", True)  # 使窗口始终位于顶层
    root.grab_set()  # 设置窗口为焦点
    label = tk.Label(root, font=('Helvetica', 48), text="")
    label.pack(padx=20, pady=20)

    countdown(remaining_seconds, label, root)

    root.mainloop()