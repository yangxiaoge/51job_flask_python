## 腾讯视频弹幕的爬虫思路
# 1. 先获取一页，封装成函数
# 2. 找到timestamp规律构建URL循环翻页，获取一集所有的页数，封装成函数
# 3. 找到target_id和vid的规律，获取12集的弹幕

import json
import time

import pandas as pd
# 导入所需库
import requests


def get_danmu_one_page(url_dm):
    """
    :param url_dm: 视频弹幕URL地址
    :return: 一页的弹幕数据
    """
    # 添加headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'cookie': 'pgv_pvid=2692477912; pgv_pvi=191707136; RK=FMgMzvwXw8; ptcz=3100d4d12df85e62687c793c550421e0511d6c4d18166d5ffd4fb8eed73af21f; tvfe_boss_uuid=e80577671ac3c06e; video_guid=e3526df0a478899e; video_platform=2; o_cookie=2315561922; pac_uid=1_2315561922; ied_qq=o2315561922; pgv_info=ssid=s605460576; pgv_si=s7903183872; _qpsvr_localtk=0.9935817137865979; ptui_loginuin=751068118; main_login=qq; vqq_access_token=35E78F7D4C963CA40691D9A921136D09; vqq_appid=101483052; vqq_openid=C9E60E4EE691057C69DD81ED500B1B0C; vqq_vuserid=1427072167; vqq_vusession=RwurmoqivNu_3kQ2w-XEyQ..; vqq_refresh_token=46C0E6F2AD094F344AA1B74CF029919F; login_time_init=2020-7-22 17:47:38; uid=825372102; vqq_next_refresh_time=5801; vqq_login_time_init=1595412058; login_time_last=2020-7-22 18:0:57',
        'referer': 'https://v.qq.com/x/cover/mzc00200iseomew/b0033m9le2c.html',
    }

    # 发起请求
    try:
        r = requests.get(url_dm, headers=headers, timeout=3)
    except Exception as e:
        print(e)
        time.sleep(3)
        r = requests.get(url_dm, headers=headers, timeout=3)

    # 解析网页
    data = json.loads(r.text, strict=False)['comments']

    # 获取评论ID
    comment_id = [i.get('commentid') for i in data]
    # 获取用户名
    oper_name = [i.get('opername') for i in data]
    # 获取会员等级
    vip_degree = [i.get('uservip_degree') for i in data]
    # 获取评论内容
    content = [i.get('content') for i in data]
    # 获取评论时间点
    time_point = [i.get('timepoint') for i in data]
    # 获取评论点赞
    up_count = [i.get('upcount') for i in data]

    # 存储数据
    df_one = pd.DataFrame({
        'comment_id': comment_id,
        'oper_name': oper_name,
        'vip_degree': vip_degree,
        'content': content,
        'time_point': time_point,
        'up_count': up_count
    })
    return df_one


def get_danmu_all_page(target_id, vid):
    """
    :param target_id: target_id
    :param vid: vid
    :return: 所有页弹幕
    """
    df_all = pd.DataFrame()
    # 记录步数
    step = 1

    for time_stamp in range(15, 100, 30):  # 右侧设置一个足够大的数
        try:  # 异常处理
            # 构建URL
            url_dm = 'https://mfm.video.qq.com/danmu?target_id={}&vid={}&timestamp={}'.format(target_id, vid,
                                                                                              time_stamp)
            # 调用函数
            df = get_danmu_one_page(url_dm)
            # 终止条件
            if df.shape[0] == 0:
                print('没有数据！')
                break
            else:
                df_all = df_all.append(df, ignore_index=True)
                # 打印进度
                print(f'我正在获取第{step}页的信息')
                step += 1
                # 休眠一秒
                time.sleep(1)
        except Exception as e:
            print(e)
            continue

    print(f'爬虫程序中止，共获取{df_all.shape[0]}条弹幕!')

    return df_all


# 获取target_id和vid，此处手动抓包获取

# 第一期上
df_1 = get_danmu_all_page(target_id='5979258600', vid='f0034cqed1f')
df_1.insert(0, 'episodes', '第一期上')

# 第一期下
df_2 = get_danmu_all_page(target_id='5977891317', vid='y00340t6k8g')
df_2.insert(0, 'episodes', '第一期下')

# 第二期上
df_3 = get_danmu_all_page(target_id='6012064484', vid='v0034wu6i8c')
df_3.insert(0, 'episodes', '第二期上')

# 第二期下
df_4 = get_danmu_all_page(target_id='6013331442', vid='m0034bdzygg')
df_4.insert(0, 'episodes', '第二期下')

# 第三期上
df_5 = get_danmu_all_page(target_id='6045300272', vid='w0034sa0mnj')
df_5.insert(0, 'episodes', '第三期上')

# 第三期下
df_6 = get_danmu_all_page(target_id='6045532740', vid='r0034sclogn')
df_6.insert(0, 'episodes', '第三期下')

# 第四期上
df_7 = get_danmu_all_page(target_id='6078160126', vid='s0034dat3nf')
df_7.insert(0, 'episodes', '第四期上')

# 第四期下
df_8 = get_danmu_all_page(target_id='6078222925', vid='u0034wv3xvg')
df_8.insert(0, 'episodes', '第四期下')

# 第五期上
df_9 = get_danmu_all_page(target_id='6111483265', vid='t003495xitz')
df_9.insert(0, 'episodes', '第五期上')

# 第五期下
df_10 = get_danmu_all_page(target_id='6111485603', vid='i0034tigcf1')
df_10.insert(0, 'episodes', '第五期下')

# 列表存储
df_list = [df_9, df_10]
# df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8,
# 循环写出
for df_name in df_list:
    # 读出数据
    epi_num = df_name['episodes'][0]
    print(f'正在写出第{epi_num}集的数据')
    df_name.to_csv(f'{epi_num}集.csv', index=True)
