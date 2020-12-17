# -*- coding: utf-8 -*-
# @Time : 2020/12/16 14:03
# @Author : Bruce Yang
# @File : you_get.py
# @Software : PyCharm
# @Description :

import threading
from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

top = Tk()
top.title("Seuic系统签名工具，made by @yangjianan")

# 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央,其中width和height为界面宽和高
width = 600
height = 519
screenwidth = top.winfo_screenwidth()
screenheight = top.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
top.geometry(alignstr)

# 阻止窗口调整大小
top.resizable(0, 0)
# 设置窗口图标
# top.iconbitmap('F:\Python\GUI界面\You-get - v0 -20190507\play_24px_1099805_easyicon.net.ico')

# 框架布局
frame_root = Frame(top)
frame_left = Frame(frame_root)
frame_right = Frame(frame_root)

frame_left.pack(side=LEFT)
frame_right.pack(side=RIGHT, anchor=N)
frame_root.pack()

# 请选择保存位置
tip2 = Label(frame_left, text='请选择保存位置：         ', font=('楷体', 25))
tip2.pack(padx=10, anchor=W)
# 保存地址输入框
input_save_address = Entry(frame_left, bg='#F7F3EC')
input_save_address.pack(ipadx=159, ipady=8, padx=20, anchor=W)


# 浏览本地文件夹，选择保存位置
def browse_folder():
    # 浏览选择本地文件夹
    save_address = filedialog.askopenfilename()
    # 把获得路径，插入保存地址输入框（即插入input_save_address输入框）
    input_save_address.insert(0, save_address)


# 为避免在下载时tkinter界面卡死，创建线程函数
def thread_it(func, *args):
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()


# “浏览文件夹”按钮
browse_folder_button = Button(frame_right, text='浏览', font=('楷体', 15), command=lambda: thread_it(browse_folder))
browse_folder_button.pack(pady=110, side=LEFT, anchor=W)
# 新建空白标签，无实际作用，内容为空，为了让界面对称，更美观，可理解为“占位符”
Label(frame_right, text='     ').pack(pady=110, side=LEFT, anchor=W)

# “开始签名”按钮
sys_sign_button = Button(frame_left, text='开始签名', font=('楷体', 15))
sys_sign_button.pack(padx=20, pady=6, anchor=W)

# ScrolledText组件（滚动文本框）
stext = ScrolledText(frame_left, width=60, height=23, background='#F7F3EC')
stext.pack(padx=20, anchor=W)

top.mainloop()
