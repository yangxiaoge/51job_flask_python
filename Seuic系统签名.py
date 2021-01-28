# -*- coding: utf-8 -*-
# @Time : 2020/12/15 19:58
# @Author : Bruce Yang
# @File : Seuic系统签名.py
# @Software : PyCharm
# @Description : PC桌面软件
# @打包exe : pyinstaller -F Seuic系统签名.py -w
import json
import os
# os.system某些命令会跳出终端,所以用subprocess
import subprocess as run
import threading
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox

# 浏览本地文件，选择apk路径
import requests

signed_apk_name = ""


def select_apk_file():
    # 浏览选择本地文件夹
    apk_path = filedialog.askopenfilename(filetypes=[(".apk", ".APK")])
    # 把获得路径，插入保存地址输入框（即插入input_save_address输入框）
    # 先清空，再输入
    et_file_path.delete(0, END)
    et_file_path.insert(0, apk_path)


# 签名按钮点击事件处理
def sign_btn():
    apk_path = et_file_path.get()
    if apk_path is None or apk_path == "":
        showwarning("警告", "请输入待签名应用路径！")
    else:
        sigh_apk(apk_path)
    # 更新新的一言
    thread_it(get_yiyan())


def install_btn():
    if signed_apk_name is None or signed_apk_name == "":
        showwarning("警告", "签名后的应用路径不存在！")
    else:
        # 脚本拼接
        command = r'{}/adb/adb.exe install -r {}'.format(os.getcwd(), signed_apk_name)
        # print('command={}'.format(command))
        # 应用安装
        result = run.call(command, shell=True)
        if result == 0:
            # 打开签名后的apk目录
            # run.call(r"start explorer /select,%s" % signed_apk_name, shell=True)
            print(signed_apk_name)
        else:
            showerror("错误", "应用安装失败！")


# 系统签名
def sigh_apk(apk_path):
    log.insert(END, "\n")
    log.insert(END, "待签名应用路径：" + apk_path + "\n")
    log.insert(END, "系统签名类型：" + sign_type.get() + "\n")
    system_signfile_path = sign_file_dir + sign_type.get()
    global signed_apk_name
    signed_apk_name = apk_path.replace('.apk', '_sys_signed.apk')
    # 脚本拼接
    command = r'java -jar {}/signapk.jar {}/platform.x509.pem {}/platform.pk8 {} {}'.format(
        system_signfile_path, system_signfile_path, system_signfile_path, apk_path, signed_apk_name
    )
    # 系统签名执行
    sys_sign_result = run.call(command, shell=True)
    if sys_sign_result == 0:
        # 打开签名后的apk目录
        # run.call(r"start explorer /select,%s" % signed_apk_name, shell=True)
        log.insert(END, "签名后应用路径：%s" % signed_apk_name + "\n")
        # 日志滚动到末尾
        log.see(END)
    else:
        showerror("错误", "系统签名失败")


def thread_it(func, *args):
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()


# 调用一言接口
def get_yiyan():
    r = requests.get("https://v1.hitokoto.cn/")
    response = r.text
    # print(response)
    data = json.loads(response)
    hitokoto = data['hitokoto']
    hitokoto_from = data['from']
    if data['from_who'] is None:
        author = ""
    else:
        author = data['from_who']
    new_text = "%s\n---%s《%s》" % (hitokoto, author, hitokoto_from)
    yiyan.config(text=new_text)


win = Tk()
win.title("Seuic系统签名工具，made by @yangjianan")

# 得到屏幕宽度
sw = win.winfo_screenwidth()
# 得到屏幕高度
sh = win.winfo_screenheight()
print("w:{} h:{}".format(sw, sh))
# pc软件的宽高
ww = 820
wh = 550
# 坐标
x = (sw - ww) // 2
y = (sh - wh) // 2

tip1 = Label(text='请选择待签名应用路径：', pady=20, font=('楷体', 25), fg='red')
tip1.pack()

# Frame布局
row = Frame(win)
row.pack(side="top", fill="both")
t1 = StringVar()
t1.set('')
# 文件路径输入框
et_file_path = Entry(row, textvariable=t1, bg='#F7F3EC')
et_file_path.pack(side=LEFT, ipadx=wh / 2, ipady=8, padx=20, pady=20, anchor=W)
# 浏览按钮
file_select = Button(row, text="浏览", font=('楷体', 22), command=select_apk_file)
file_select.pack(side=LEFT, after=et_file_path)

# 创建一个 系统签名类型 下拉列表
sign_type = StringVar()
numberChosen = Combobox(win, width=20, textvariable=sign_type, state='readonly')
sign_file_dir = os.getcwd() + r'/系统签名/'
# print("sign_file_dir={}".format(os.listdir(sign_file_dir)))
numberChosen['values'] = os.listdir(sign_file_dir)  # 设置下拉列表的值
numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
numberChosen.pack()

# 签名按钮
btn = Button(text="开始签名", font=('楷体', 22), command=sign_btn)
btn.pack(ipadx=10, ipady=5, pady=10)

# 安装签名后的应用按钮
install_btn = Button(text="安装签名应用", font=('楷体', 22), command=install_btn)
install_btn.pack(pady=10, after=btn)

# 日志显示
log = ScrolledText(height="10")
log.pack()

# 一言
yiyan = Label(text="强大使人快乐。", font=('楷体', 25), fg='green')
yiyan.pack(side=BOTTOM)

win.geometry("{}x{}+{}+{}".format(ww, wh, x, y))

thread_it(get_yiyan)

# 阻止窗口调整大小
# win.resizable(0, 0)
# 设置窗口图标
win.iconbitmap(os.getcwd() + r'/favicon.ico')
# 进入消息循环
win.mainloop()
