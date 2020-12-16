# -*- coding: utf-8 -*-
# @Time : 2020/11/30 15:12
# @Author : Bruce Yang
# @File : 王者荣耀皮肤.py
# @Software : PyCharm
# @Description :

import os
import re

import requests
from lxml import etree


def get_index():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'referer': 'https://pvp.qq.com/web201605/wallpaper.shtml'
    }
    url = 'https://pvp.qq.com/web201605/herolist.shtml'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('gbk')
    else:
        return None


def parse_index(html):
    selector = etree.HTML(html)
    links = selector.xpath('//*[@class="herolist clearfix"]/li/a/@href')
    links = ['https://pvp.qq.com/web201605/' + link for link in links]
    return links


def parse_deatil(url):
    response = requests.get(url)
    html = response.content.decode('gbk')
    name = re.findall(r'<h2 class="cover-name">(.*?)</h2>', html, re.S)
    id = re.findall(r'<span class="hidden">(\d+)</span>', html, re.S)
    skin_name_str = re.findall(r'<ul class="pic-pf-list pic-pf-list3" data-imgname="(.*?)">', html, re.S)
    skin_name_list = skin_name_str[0].split('|')
    skin_name_list = [name.split('&')[0] for name in skin_name_list]

    dir_name = '王者荣耀皮肤'
    # 保存目录
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    for i, skin_name in enumerate(skin_name_list):
        skin_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'.format(id[0], id[0],
                                                                                                           i + 1)
        file_name = '{}.jpg'.format(skin_name)
        res = requests.get(skin_url)
        if not os.path.exists(dir_name + '/' + name[0]):
            os.mkdir(dir_name + '/' + name[0])
        with open(dir_name + '/' + name[0] + '/' + file_name, 'wb') as f:
            f.write(res.content)
    print('正在爬取：{}{}'.format(name[0], skin_name_list))


if __name__ == '__main__':
    html = get_index()
    for link in parse_index(html):
        parse_deatil(link)
