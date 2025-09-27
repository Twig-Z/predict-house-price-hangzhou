#coding=utf-8
import re
import csv

import numpy as np
import pandas as pd

name = "hangzhou"

file_path = 'E:\\data\\{}\\data_processing\\{}_clean.csv'.format(name, name)
outputfile = "E:\\data\\{}\\data_processing\\{}_train.csv".format(name, name)

# 数据加载
miss_value = ["null", "暂无数据"]
df = pd.read_csv(file_path, na_values=miss_value, encoding='utf-8')

df = df.drop(['id', '交通情况', '产权所属', '抵押信息', '房屋户型',
              '所在楼层', '配备电梯', '楼层高度', '用水类型', '用电类型', '燃气价格'], axis=1)
df.to_csv(outputfile, encoding='utf-8', index=False)