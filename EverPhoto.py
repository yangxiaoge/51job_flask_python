# -*- coding: utf-8 -*-
# @Time : 2020/11/13 14:06
# @Author : Bruce Yang
# @File : EverPhoto.py
# @Software : PyCharm
# @Description : 时光相册签到

import json
import sys

import requests


def start(mobile, pwd, server_jiang):
    header = {
        "User-Agent": "EverPhoto/2.7.6 (Android;2702;ONEPLUS A6000;28;oppo)",
        "x-device-mac": "02:00:00:00:00:00",
        "application": "tc.everphoto",
        "authorization": "Bearer 94P6RfZFfqvVQ2hH4jULaYGI",
        "x-locked": "1",
        "content-length": "0",
        "accept-encoding": "gzip"
    }
    url = "https://api.everphoto.cn/users/self/checkin/v2"
    urllogin = "https://web.everphoto.cn/api/auth"
    loginkey = {
        "mobile": mobile,
        "password": pwd  # 在登录界面按F12，然后点登录，查看[color=#ff0000]"auth"里面[/color]手机号后面的加密密码
    }
    responselogin = requests.post(urllogin, loginkey, headers=header)
    res_json = json.loads(responselogin.text)
    # print(res_json)
    logindata = res_json["data"]
    header["authorization"] = "Bearer " + logindata["token"]
    response = requests.post(url, headers=header)
    datas = json.loads(response.text)
    # print(datas)
    # print(datas["data"]["checkin_result"])
    code = datas["code"]
    checkin_result = datas["data"]["checkin_result"]
    total_reward = str(datas["data"]["total_reward"] // 1024 // 1024) + "M"
    tomorrow_reward = str(datas["data"]["tomorrow_reward"] // 1024 // 1024) + "M"
    if code == 0:
        if checkin_result:
            result_msg = "签到成功"
        else:
            result_msg = "已签到过或签到失败"
    else:
        result_msg = "签到失败"

    # 签到结果通过server酱推送到微信
    serverUrl = "https://sc.ftqq.com/%s.send" % server_jiang
    data = {
        "text": "时光相册：" + result_msg,
        "desp": "累计奖励：" + total_reward + " ，明日奖励：" + tomorrow_reward
    }
    requests.post(serverUrl, data)

    return data["text"] + "\n" + data["desp"]


if __name__ == '__main__':
    # print("参数：" + str(sys.argv))
    log = start(sys.argv[1], sys.argv[2], sys.argv[3])
    print(log)
