# -*- coding: utf-8 -*-
# @Time : 2020/11/28 10:13
# @Author : Bruce Yang
# @File : mm_contact.py
# @Software : PyCharm
# @Description : 查询微信删除我的人

import time

from appium import webdriver


# 判断元素是否存在
def is_element_exist(element, timeout=3):
    count = 0
    while count < timeout:
        souce = driver.page_source
        if element in souce:
            return True
        else:
            count += 1
            time.sleep(1)
    return False


desired_caps = {
    "platformName": "Android",  # 系统
    "platformVersion": "9",  # 系统本号
    "deviceName": "MI6",  # 设备名
    "appPackage": "com.tencent.mm",  # 包名
    "appActivity": ".ui.LauncherUI",  # app 启动时主 Activity
    'unicodeKeyboard': True,  # 使用自带输入法
    'noReset': True  # 保留 session 信息，可以避免重新登录
}


# 上拉方法
def swipe_up(distance, time):  # distance为滑动距离，time为滑动时间
    width = 1080
    height = 1920  # width 和 height根据不同手机而定
    driver.swipe(1 / 2 * width, 9 / 10 * height, 1 / 2 * width, (9 / 10 - distance) * height, time)


# 获取通讯录列表
def get_address_list(flag):
    if flag == True:
        driver.find_elements_by_id('com.tencent.mm:id/cn_')[1].click()
        time.sleep(2)
        # 上滑
        swipe_up(1 / 2, 2000)
    else:
        swipe_up(5 / 6, 2000)
    time.sleep(2)
    # 获取昵称（备注）
    address_list = driver.find_elements_by_id('com.tencent.mm:id/dy5')
    remarks = []
    for address in address_list:
        remark = address.get_attribute("content-desc")
        # 排除自己和微信官方号
        if remark != "appium" and "微信" not in remark:
            remarks.append(remark)
    return remarks


# 判断是否被删
def is_delete(remark, count):
    if count == "1":
        time.sleep(1)
        print('点击微信搜索框')
        driver.find_element_by_id('com.tencent.mm:id/cn1').click()
    time.sleep(1)
    print('在搜索框输入搜索信息')
    driver.find_element_by_id('com.tencent.mm:id/bhn').send_keys(remark)
    time.sleep(0.6)
    print('点击搜索到的好友')
    driver.find_element_by_id('com.tencent.mm:id/tm').click()
    time.sleep(0.6)
    # 转账
    driver.find_element_by_id('com.tencent.mm:id/aks').click()
    time.sleep(0.6)
    driver.find_elements_by_id('com.tencent.mm:id/pa')[5].click()
    time.sleep(0.6)
    driver.find_element_by_id('com.tencent.mm:id/cx_').click()
    time.sleep(0.8)
    driver.find_element_by_id('com.tencent.mm:id/cxi').click()
    time.sleep(0.8)
    # 判断是否被删
    is_exist = is_element_exist('com.tencent.mm:id/jh')
    if is_exist is True:
        return remark
    else:
        return False


# 返回搜索框
def search_back():
    time.sleep(1)
    driver.find_element_by_id('com.tencent.mm:id/dn').click()
    time.sleep(1)
    driver.find_element_by_id('com.tencent.mm:id/rs').click()
    time.sleep(1)
    # 清除搜索框，输入下一个
    driver.find_element_by_id('com.tencent.mm:id/fsv').click()


# 删除把自己删除的人
def del_person(nicks):
    for inx, val in enumerate(nicks):
        time.sleep(2)
        if inx == 0:
            print('在搜索框输入搜索信息')
            driver.find_element_by_id('com.tencent.mm:id/bhn').send_keys(val)
        else:
            time.sleep(2)
            print('点击微信搜索框')
            driver.find_element_by_id('com.tencent.mm:id/cn1').click()
            print('在搜索框输入搜索信息')
            time.sleep(1)
            driver.find_element_by_id('com.tencent.mm:id/bhn').send_keys(val)
        time.sleep(2)
        print('点击搜索到的人')
        driver.find_element_by_id('com.tencent.mm:id/tm').click()
        time.sleep(2)
        print('点击聊天对话框右上角...')
        driver.find_element_by_id('com.tencent.mm:id/cj').click()
        time.sleep(2)
        print('点击头像')
        driver.find_element_by_id('com.tencent.mm:id/f3y').click()
        time.sleep(2)
        print('点击联系人右上角...')
        driver.find_element_by_id('com.tencent.mm:id/cj').click()
        time.sleep(2)
        print('点击删除按钮')
        driver.find_element_by_id('com.tencent.mm:id/g6f').click()
        time.sleep(2)
        print('点击弹出框中的删除')
        driver.find_element_by_id('com.tencent.mm:id/doz').click()


if __name__ == '__main__':
    remarks = []
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    time.sleep(10)
    # remarks1 = get_address_list(True)
    # remarks.extend(remarks1)
    # while True:
    #     # 是否到了通讯录末尾
    #     is_end = is_element_exist('com.tencent.mm:id/azb')
    #     time.sleep(2)
    #     remarks2 = get_address_list(False)
    #     remarks.extend(remarks2)
    #     if is_end == True:
    #         break
    remarks = set(
        {'于诗雯', '潘洋', '曾  曾', '刁文阳', '董品', '轻薄的假面', '张贵兵', '杨冰洁', '王墨'})
    print("通讯录昵称列表：", remarks)
    time.sleep(5)
    dels = []
    for inx, val in enumerate(remarks):
        rt = ""
        if inx == 0:
            rt = is_delete(val, "1")
        else:
            rt = is_delete(val, "")
        if rt is False:
            # 返回搜索框
            driver.keyevent(4)
            search_back()
        # 被删除
        else:
            dels.append(rt)
            time.sleep(2)
            driver.find_element_by_id('com.tencent.mm:id/doz').click()
            search_back()
    print("删除我的人：", dels)
    # 删除删了自己的人
    del_person(dels)
