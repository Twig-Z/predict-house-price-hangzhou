import pandas as pd
name = "hangzhou"

file_path = 'E:\\data\\{}\\data_processing\\{}.origin.csv'.format(name,name)
outputfile = "E:\\data\\{}\\data_processing\\{}_quchong.csv".format(name,name)
chongfu = "E:\\data\\{}\\data_processing\\{}_chongfu.csv".format(name,name)

def detect_duplicate_rows(csv_file_path, encoding='utf-8', sep=','):
    try:
        # 读取CSV文件
        df = pd.read_csv(csv_file_path, encoding=encoding, sep=sep)

        # 检查是否有行
        if df.empty:
            print("CSV文件为空")
            return df, pd.DataFrame(), df

        # 标识重复行
        duplicate_mask = df.duplicated(keep='first')

        # 找出所有重复行（包括第一次出现）
        all_duplicates_mask = df.duplicated(keep=False)
        # 获取重复行（包括第一次出现的行）
        duplicate_rows = df[all_duplicates_mask].copy()
        # 获取唯一行
        unique_rows = df[~all_duplicates_mask].copy()

        # 打印结果信息
        if duplicate_rows.empty:
            print("没有找到重复行")
        else:
            print(f"找到 {duplicate_rows.shape[0]} 行重复数据")
            # 按重复组排序以便于查看
            duplicate_rows = duplicate_rows.sort_values(by=list(duplicate_rows.columns))

        return df, duplicate_rows, unique_rows

    except Exception as e:
        print(f"处理CSV文件时出错: {e}")
        return None, None, None

def delete_duplicate_rows(csv_file_path):
    df = pd.read_csv(csv_file_path, header=0)
    #删除重复行
    datalist = df.drop_duplicates()

    datalist.to_csv(outputfile, index=False, encoding='utf-8')




def main():
    # 示例用法
    #file_path = r"C:\Users\zhang-jingwen\Desktop\hangzhou.origin.csv"  # 替换为实际CSV文件路径

    # 如果CSV文件使用不同的编码或分隔符，请相应修改这些参数
    # 例如，中文CSV可能使用GBK编码，某些CSV可能使用制表符(\t)分隔
    original_df, duplicates_df, unique_df = detect_duplicate_rows(
        file_path,
        encoding='utf-8',  # 可选: 'gbk', 'gb2312', 'utf-8-sig' 等
        sep=','  # 可选: '\t', ';' 等
    )

    if duplicates_df is not None and not duplicates_df.empty:
        print("\n重复行预览:")
        print(duplicates_df.head())
        # 将重复行保存到新的CSV文件
        duplicates_df.to_csv(chongfu, encoding='utf-8')
        print("重复行已保存到'chongfu.csv'")

        #删除重复行，另存
        delete_duplicate_rows(file_path)
        print("去重结果已保存到‘{}_quchong.csv".format(name))




if __name__ == "__main__":
    main()