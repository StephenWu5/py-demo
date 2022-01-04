# -*- coding: utf-8 -*-
import pandas
import jieba
import re

# loading data
data = pandas.read_csv(
    "./movie.csv"
)

# 1.文本内容清洗，清楚特殊符号，用正则表达式
pattern = r"[!\"#$%&'()*+,-./:;<=>?@[\\\]^_^{|}~—！，。？、￥…（）：【】《》‘’“”\s]+"
re_obj = re.compile(pattern)
def clear(text):
    return re.sub(pattern, "", text)
data['内容'] = (" ".join('%s' %id for id in data['内容']))
print(type(data['内容']), 'data')
data['内容'] = data['内容'].apply(clear)
print(data.head())

def cut_word(text):  # 返回生成器
    return jieba.cut(text)
# 2.分词 用jieba来实现分词
data['内容'] = data['内容'].apply(cut_word)

# 3.停用词处理，这里我用的是中文停词用表（文末附）
def get_stopword():  # 使用set
    s = set()
    with open('./cn_stopwords.txt', encoding='UTF-8') as f:
        for line in f:
            s.add(line.strip())
    return s
def remove_stopword(words):
    return [word for word in words if word not in stopword]
stopword = get_stopword()
data['内容'] = data['内容'].apply(remove_stopword)

# 4.词汇统计
from itertools import chain
from collections import Counter
li_2d = data['内容'].tolist()
# 将二维列表转换为一维
li_1d = list(chain.from_iterable(li_2d))
print(f'总词汇量：{len(li_1d)}')
c = Counter(li_1d)
print(f'不重复词汇量：{len(c)}')
common = c.most_common(50)
# print(common)
import pandas as pd
frame = pd.DataFrame(common)
file = frame.to_csv('common11.csv')
# 计算每个评论的用词数
num = [len(li) for li in li_2d]

import matplotlib.pyplot as plt
# 绘制所有用户在评论时所用词汇书，绘制直方图
# n, bins, patches = plt.hist(num, bins=20, alpha=0.5)
# plt.yscale('log')
# plt.show()

# 生成词云图
from wordcloud import WordCloud
# 导入图像处理库
import PIL.Image as image
# 导入数据处理库
import numpy as np
import matplotlib.colors as colors  # 处理图片相关内容
# 文末附颜色对照表
colormaps = colors.ListedColormap(['#FF4500', '#FF7F50', '#FFD700'])
# mask可以用PPT画自己想要的图形（我这里是用来“长津湖”的艺术字）
mask1 = np.array(image.open('./word_cloud.png'))
wc = WordCloud(font_path="./SIMYOU.TTF", background_color="white",
               mask=mask1, colormap=colormaps)
img = wc.generate_from_frequencies(c)
plt.figure(figsize=(15, 10))
plt.imshow(img)
plt.axis('off')
plt.show()
