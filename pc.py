# -*- coding: utf-8 -*-
# @Time : 2020/12/15 19:58
# @Author : Bruce Yang
# @File : pc.py
# @Software : PyCharm
# @Description : PC桌面软件

import tkinter

import windnd

win = tkinter.Tk(className="系统签名工具")

# 得到屏幕宽度
sw = win.winfo_screenwidth()
# 得到屏幕高度
sh = win.winfo_screenheight()
print("w:{} h:{}".format(sw, sh))
# pc软件的宽高
ww = 500
wh = 300
# 坐标
x = (sw - ww) / 2
y = (sh - wh) / 2

t1 = tkinter.StringVar()
t1.set('')
et = tkinter.Entry(textvariable=t1, width=50)
et.pack()
btn = tkinter.Button(text="确认")
btn.pack()

win.geometry("{}x{}+{}+{}".format(ww, wh, int(x), int(y)))


def dragged_file(files):
    msg = "\n".join((item.decode('gbk') for item in files))
    # showinfo("拖放的文件", msg)
    t1.set(msg)


windnd.hook_dropfiles(win, func=dragged_file)
# 进入消息循环
win.mainloop()
