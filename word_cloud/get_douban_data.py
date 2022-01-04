#!/usr/bin/python
# -*- coding: utf-8 -*-
# 导入工具包
import io
import sys
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

headers = {
    'cookie':'bid=6K3A_jjiN80; ll="118282"; dbcl2="163506500:oGQORQHIfDg"; ck=2dlX; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1641180000%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.2058072063.1641180001.1641180001.1641180001.1; __utmb=30149280.0.10.1641180001; __utmc=30149280; __utmz=30149280.1641180001.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1559159524.1641180001.1641180001.1641180001.1; __utmb=223695111.0.10.1641180001; __utmc=223695111; __utmz=223695111.1641180001.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=D617E2A55D08D125189880CCA1992B20E|72b9976c16a5385edb2568a5230a6017; _pk_id.100001.4cf6=daca4f8f9fd3ee11.1641180000.1.1641180097.1641180000',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}
# url = 'https://movie.douban.com/subject/25845392/collections?start=20'

# url = ['https://movie.douban.com/subject/25845392/comments?start={}&limit=20&status=P&sort=new_score'.format(i) for i in range(0, 50, 20)] 长津湖

url = ['https://movie.douban.com/subject/32579501/comments?start={}&limit=20&status=P&sort=new_score'.format(i) for i in range(0, 50, 20)]

# 空list
lis = []

for urli in url:
    response = requests.get(urli, headers=headers).text
    bs4 = BeautifulSoup(response, 'html.parser')
    # 信息
    # 用户
    names = bs4.select('#comments > div > div.comment > h3 > span.comment-info > a')
    # 评级
    pingjis = bs4.select('#comments > div > div.comment > h3 > span.comment-info')
    # 日期
    riqis = bs4.select('#comments > div > div.comment > h3 > span.comment-info > span.comment-time')
    # 内容
    neirongs = bs4.select('#comments > div > div.comment > p > span')
    for name, pingji, riqi, neirong in zip(names, pingjis, riqis, neirongs):
        pingji_re = pingji.find_all('span')
        lis.append([name.get_text(),
                    pingji_re[1]['class'],
                    pingji_re[1]['title'],
                    riqi.get_text().strip(),
                    neirong.get_text()])
    print('完成:', urli)
    time.sleep(np.random.randint(5, 10))
with open("movie_sc.txt","a+") as f:
            f.write(str(lis)+" "+"\n\n")

result2 = pd.DataFrame(lis, columns=['用户', '评级', '等级', '日期', '内容'])
# 写入excel
frame = pd.DataFrame(result2)
file = frame.to_csv('movie.csv')


# for x in bs4.select(".comment-content .short"):
#         with open("movie_sc.txt","a+") as f:
#             f.write(str(x.get_text())+" "+"\n\n")