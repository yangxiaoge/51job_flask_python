# -*- coding: utf-8 -*-
# @Time : 2020/12/15 19:58
# @Author : Bruce Yang
# @File : Seuic系统签名.py
# @Software : PyCharm
# @Description : PC桌面软件
import os
# os.system某些命令会跳出终端,所以用subprocess
import subprocess as run
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
    print("\n")
    system_signfile_path = os.getcwd() + r'/系统签名/通用签名'
    signed_apk_name = apk_path.replace('.apk', '_sys_signed.apk')
    # 脚本拼接
    command = r'java -jar {}/signapk.jar {}/platform.x509.pem {}/platform.pk8 {} {}'.format(
        system_signfile_path, system_signfile_path, system_signfile_path, apk_path, signed_apk_name
    )
    # 系统签名执行
    sys_sign_result = run.call(command, shell=True)
    if sys_sign_result == 0:
        # 打开签名后的apk目录
        run.call(r"start explorer /select,%s" % signed_apk_name, shell=True)
    else:
        showerror("错误", "系统签名失败")


# 浏览本地文件夹，选择保存位置
def browse_folder():
    # 浏览选择本地文件夹
    apk_path = filedialog.askopenfilename()
    # 把获得路径，插入保存地址输入框（即插入input_save_address输入框）
    # 先清空，再输入
    et_file_path.delete(0, 'end')
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
win.iconbitmap(r'D:\workspace\python\demo\shixun\51job_flask\favicon.ico')
# 进入消息循环
win.mainloop()
