import csv

import pandas as pd
import glob

name = "hangzhou"

outputfile = 'E:\\data\\{}\\data_processing\\{}.origin.csv'.format(name,name)

csv_list = glob.glob('E:\\data\\{}\\data_origin\\*.csv'.format(name))
print(u'共发现%s个CSV文件' % len(csv_list))
print(u'正在处理............')


'''def hebing():
    for inputfile in csv_list:
        f = open(inputfile,'r',encoding='utf-8')
        data = pd.read_csv(f)
        data.to_csv(outputfile, mode='a', index=False, header=None, encoding='utf-8')
    print('完成合并')
'''
def hebing():
    merged_data = []

    for inputfile in csv_list:
        with open(inputfile, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            file_data = list(csv_reader)
        file_data = file_data[1:]
        merged_data += file_data

    with open(outputfile, 'w', newline='', encoding='utf-8') as merged_file:
        data = [
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
        writer = csv.writer(merged_file)
        writer.writerow(data)
        csv_writer = csv.writer(merged_file)
        csv_writer.writerows(merged_data)

    print('完成合并')



if __name__ == '__main__':
    hebing()
