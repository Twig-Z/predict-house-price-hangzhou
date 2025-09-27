#coding=utf-8
import re
import csv

name = "hangzhou"

file_path = 'E:\\data\\{}\\data_processing\\{}_quchong.csv'.format(name, name)
outputfile = "E:\\data\\{}\\data_processing\\{}_duiqi.csv".format(name, name)


def contains_chinese(text):
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False


with open(file_path, encoding="utf-8", errors='replace') as f:
    reader = csv.reader(f)
    next(reader)
    context = [line for line in reader]

with (open(outputfile, "w", encoding="utf-8", newline="") as f):
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
    writer = csv.writer(f)
    writer.writerow(data)

    for line in context:
        # 去除每个数据项的空白符和换行符
        line = [x.strip() for x in line]

        '''# 如果是表头或数据项中包含非数值数据（如'总价'、'单价'等），直接写入，不做转换
        if line and (line[0] == "id" or "总价" in line or "单价" in line):
            writer.writerow(line)
            continue'''

        # 备份原始记录，便于后续字段重排时使用
        line_copy = line[:]

        # 处理交通情况
        if not contains_chinese(line[4]):
            line[4] = "null"

        # 处理没有房源编码的项
        if contains_chinese(line[15]):
            line[15] = "null"
            cnt = 16
            while cnt <= 30:
                #print(cnt)
                line[cnt] = line_copy[cnt - 1] if len(line_copy) > cnt - 1 else "null"
                cnt += 1

        # 备份原始记录，便于后续字段重排时使用
        line_copy = line[:]

        # 处理“别墅”记录：调整字段位置
        if line[10] == "别墅":
            #print(line)
            '''while len(line) < 26:
                line.append("null")'''
            # 对字段进行重排（参考原有逻辑）
            line[19] = "null"
            line[20] = line_copy[19] if len(line_copy) > 19 else "null"
            line[21] = "null"
            line[22] = line_copy[20] if len(line_copy) > 20 else "null"
            line[23] = line_copy[21] if len(line_copy) > 21 else "null"
            line[24] = line_copy[22] if len(line_copy) > 22 else "null"
            line[25] = line[26] = "null"
            line[27] = line_copy[24] if len(line_copy) > 24 else "null"
            line[28] = line[29] = line[30] = "null"

        # 处理“车库”记录：调整字段位置
        if line[10] == "车库":
            '''while len(line) < 26:
                line.append("null")'''
            #print(line)
            line[17] = line_copy[16] if len(line_copy) > 16 else "null"
            line[18] = line_copy[17] if len(line_copy) > 17 else "null"
            line[22] = line_copy[18] if len(line_copy) > 18 else "null"
            num_null = [16, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30]
            for number in num_null:
                line[number] = "null"

        try:
            # 将总价数据项统一整理为整数，确保索引存在且数据为数值
            if len(line) > 5 and line[5].replace('.', '', 1).isdigit():
                float_num = float(line[5])
                line[5] = str(int(float_num))

            # 去除单价数据项单位
            if len(line) > 6:
                line[6] = line[6].split("元/平")[0]

            # 去除建筑面积数据项的单位（确保不为空或“暂无数据”）
            if len(line) > 18 and line[18] not in ["null", "暂无数据"]:
                line[18] = line[18].split("㎡")[0]

            # 去除套内面积数据项的单位
            if len(line) > 20 and line[20] not in ["null", "暂无数据"]:
                line[20] = line[20].split("㎡")[0]

            writer.writerow(line)
        except Exception as e:
            print("数据项转换失败!该记录未写入", e)
