# -*- coding: utf-8 -*-
# @Time : 2020/12/15 19:58
# @Author : Bruce Yang
# @File : pc.py
# @Software : PyCharm
# @Description : PC桌面软件

from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import *


# 选择apk文件
def select_apk_file():
    apk_path = et_file_path.get()
    if apk_path is None or apk_path == "":
        showwarning("警告", "请输入待签名应用路径！")
    else:
        sigh_apk(apk_path)


# 系统签名
def sigh_apk(apk_path):
    print(apk_path)


# 浏览本地文件夹，选择保存位置
def browse_folder():
    # 浏览选择本地文件夹
    apk_path = filedialog.askopenfilename()
    # 把获得路径，插入保存地址输入框（即插入input_save_address输入框）
    et_file_path.insert(0, apk_path)


win = Tk()
win.title("Seuic系统签名工具，made by @yangjianan")

# 得到屏幕宽度
sw = win.winfo_screenwidth()
# 得到屏幕高度
sh = win.winfo_screenheight()
print("w:{} h:{}".format(sw, sh))
# pc软件的宽高
ww = 600
wh = 350
# 坐标
x = (sw - ww) / 2
y = (sh - wh) / 2

tip1 = Label(text='请选择待签名应用路径：', pady=20, font=('楷体', 25), fg='red')
tip1.pack()

# Frame布局
row = Frame(win)
row.pack(side="top", fill="both")
t1 = StringVar()
t1.set('')
# 文件路径输入框
et_file_path = Entry(row, textvariable=t1, width=20, bg='#F7F3EC')
et_file_path.pack(side=LEFT, ipadx=150, ipady=8, padx=20, pady=20, anchor=W)
# 浏览按钮
file_select = Button(row, text="浏览", font=('楷体', 22), command=browse_folder)
file_select.pack(side=LEFT, after=et_file_path)
# 签名按钮
btn = Button(text="开始签名", font=('楷体', 22), command=select_apk_file)
btn.pack(ipadx=50, ipady=8, padx=20, pady=20)

win.geometry("{}x{}+{}+{}".format(ww, wh, int(x), int(y)))

# 阻止窗口调整大小
# win.resizable(0, 0)
# 设置窗口图标
# win.iconbitmap('F:\Python\GUI界面\You-get - v0 -20190507\play_24px_1099805_easyicon.net.ico')
# 进入消息循环
win.mainloop()
