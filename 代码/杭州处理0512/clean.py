#coding=utf-8
import re
import csv

import numpy as np
import pandas as pd

name = "hangzhou"

file_path = 'E:\\data\\{}\\data_processing\\{}_duiqi.csv'.format(name, name)
outputfile = "E:\\data\\{}\\data_processing\\{}_clean.csv".format(name, name)

# 数据加载
miss_value = ["null", "暂无数据"]
df = pd.read_csv(file_path, na_values=miss_value, encoding='utf-8')


# 清洗文本字段
def clean_text(text):
    """清理特殊字符和空白"""
    return re.sub(r'_x000D_<br>|\s+', '', str(text)).strip()


text_cols = [
    "id", "小区名称", "所在区域", "所在位置",
    "交通情况", "总价", "单价",

    "挂牌时间", "交易权属", "上次交易", "房屋用途",
    "房屋年限", "产权所属", "抵押信息", "房本备件",
    "房源编码",

    "房屋户型", "所在楼层", "建筑面积", "户型结构",
    "套内面积", "建筑类型", "房屋朝向", "建筑结构",
    "装修情况", "梯户比例", "配备电梯", "楼层高度",
    "用水类型", "用电类型", "燃气价格",
]
for col in text_cols:
    df[col] = df[col].apply(clean_text)
# 特征工程
# 处理房屋户型
df['卧室数'] = df['房屋户型'].apply(lambda x: int(re.search(r'(\d+)室', x).group(1)) if re.search(r'(\d+)室', x) else 0)
df['客厅数'] = df['房屋户型'].apply(lambda x: int(re.search(r'(\d+)厅', x).group(1)) if re.search(r'(\d+)厅', x) else 0)
df['卫生间数'] = df['房屋户型'].apply(
    lambda x: int(re.search(r'(\d+)卫', x).group(1)) if re.search(r'(\d+)卫', x) else 0)


# 处理所在楼层
def parse_floor(text):
    floor_map = {'低楼层': 1, '中楼层': 2, '高楼层': 3}
    floor_pos = 2
    # 新增正则表达式来匹配低、中、高楼层的英文描述
    match = re.match(r'(\b中楼层\b|\b低楼层\b|\b高楼层\b)', text)
    if match:
        floor_pos = floor_map[match.group()]
        #print(floor_pos)
    else:
        print(text)

    total_floor = int(re.search(r'共(\d+)层', text).group(1)) if re.search(r'共(\d+)层', text) else np.nan

    return floor_pos, total_floor


df[['楼层位置', '总层数']] = df['所在楼层'].apply(lambda x: pd.Series(parse_floor(x)))

# 处理建筑/套内面积
df['建筑面积'] = (
    df['建筑面积']
    .str.replace('㎡', '', regex=False)
    .str.replace('_x000D_', '', regex=False)
    .str.strip()
)
df['建筑面积'] = pd.to_numeric(df['建筑面积'], errors='coerce')

df['套内面积'] = (
    df['套内面积']
    .str.replace('㎡', '', regex=False)
    .str.replace('_x000D_', '', regex=False)
    .str.strip()
    .replace('暂无数据', np.nan)
)
df['套内面积'] = pd.to_numeric(df['套内面积'], errors='coerce')

# 面积空值填补
df['建筑面积'] = df['建筑面积'].fillna(df['建筑面积'].median())
df['套内面积'] = df['套内面积'].fillna(df['套内面积'].median())

df['得房率'] = df['套内面积'] / df['建筑面积']

# 处理抵押信息
df['是否有抵押'] = df['抵押信息'].apply(lambda x: 1 if '有抵押' in x else 0)
df['抵押金额'] = df['抵押信息'].apply(
    lambda x: float(re.search(r'(\d+)万元', x).group(1)) if re.search(r'(\d+)万元', x) else 0)


# 处理交通信息
def parse_station(text):
    if ')' in text:
        index = text.find(')')
        #print(index)
        station = text[index + 1:].strip()
    else:
        # 如果没有右括号，提取号线右边的内容
        station = text.split('号线')[-1].strip()
    return station


df['是否地铁'] = df['交通情况'].apply(lambda x: 1 if '近地铁' in x else 0)
df['临近地铁站'] = df['交通情况'].apply(lambda x: parse_station(x) if '近地铁' in x else 0)


# 其他特征
df['是否电梯'] = df['配备电梯'].map({'有': 1, '无': 0})
df['是否电梯'] = df['是否电梯'].fillna(0)

df['产权类型'] = df['产权所属'].map({'非共有': 0, '共有': 1, '暂无数据': 0})
df['产权类型'] = df['产权类型'].fillna(0)

# 只删掉总价为空的行
df = df.dropna(subset=['总价'])
df = df.drop(['id', '房源编码'], axis=1)
df.to_csv(outputfile, encoding='utf-8')
