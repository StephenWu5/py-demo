#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import sys
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import jieba
import matplotlib.pyplot as plt
fig, ax=plt.subplots()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

def GetWordCloud():
    path_txt = "./movie_sc.txt";
    path_img = "./word_cloud.png";
    f = open(path_txt, 'r', encoding='UTF-8').read()
    background_image = np.array(Image.open(path_img))
    cut_text = " ".join(jieba.cut(f))

    wordcloud = WordCloud(
        font_path="/home/wuxs/A我的数据盘/06project/py-demo/SIMYOU.TTF",
        background_color="white",
        mask=background_image
    ).generate(cut_text)

    ax.imshow(wordcloud)
    ax.axis("off")
    plt.show()
    wordcloud.to_file(r"word_cloud_result.png")


if __name__ == '__main__':
    GetWordCloud()