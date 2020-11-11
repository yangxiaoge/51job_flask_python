# -*- coding = utf-8 -*-
# @Time : 2020/11/10 19:20
# @Author : Bruce Yang
# @File : job51_spider.py
# @Software : PyCharm
# @Description :

import datetime
import json
import re

import requests
from bs4 import BeautifulSoup

# 正则
search_result = re.compile(r',"engine_search_result":(.*?),"jobid_count":"', re.S)

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/86.0.4240.75 Safari/537.36"
}


# 查询岗位
def search_job(jobName):
    start_time = datetime.datetime.now()

    job_list = []
    # 取50页数据，知道某一页数据为0时
    for index in range(1, 200):
        # for index in range(1, 2):
        print("查询第%d页。。。" % index)
        url = 'https://search.51job.com/list/070200,000000,0000,00,9,99,' + str(jobName) + ',2,' + str(index) + '.html'
        html = get_page_html(url)
        # print(html)

        # 通过正则找到招聘公司数据
        jobs_result = re.findall(search_result, html)
        # print(jobs_result[0])

        # 进行json格式的编码, 将列表转化为字符串
        json_str = json.dumps(jobs_result[0])
        # print(json_str)
        # 将 JSON 数组转换为 Python 字典（解析数组调用两次json的loads方法）
        data = json.loads(json.loads(json_str))
        print("岗位数：%d" % len(data))
        if len(data) <= 0:
            print("没有数据了，查询结束")
            break

        for iData in data:
            # print(iData)

            job_item = {'company_name': iData['company_name'],
                        'providesalary_text': iData['providesalary_text'],
                        'attribute_text': iData['attribute_text'],
                        'job_href': iData['job_href'],
                        'job_info': job_detail(iData['job_href'])}
            # print(job_item)
            job_list.append(job_item)

    end_time = datetime.datetime.now()
    print("查询岗位总耗时%d秒" % (end_time - start_time).seconds)

    return json.dumps(job_list)


# 工作详情
def job_detail(job_url):
    html = get_page_html(job_url)
    bs = BeautifulSoup(html, "html.parser")
    infos = bs.select('.tCompany_main > .tBorderTop_box > .bmsg.job_msg.inbox > p')
    info_str = ""
    for i in infos:
        # print(type(i))
        # print(i.get_text())
        info_str += i.text.strip() + "\n"

    address = bs.select('.tCompany_main > .tBorderTop_box > .bmsg.inbox > .fp')
    address_str = ""
    for ii in address:
        address_str += ii.text.strip()

    job_info = f'职位信息：\n{info_str}\n{address_str}'
    # print(job_info)
    return job_info


# 获取页面html
def get_page_html(url):
    r = requests.get(url, headers=header)
    r.encoding = 'gbk'
    return r.text


if __name__ == '__main__':
    job = input("请输入要搜索的职位：")
    search_job(job)
