import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Scatter
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
name = "hangzhou"
chengshi = "杭州"

file_path = 'E:\\data\\{}\\data_processing\\{}_clean.csv'.format(name, name)
miss_value = ["null", "暂无数据"]
data = pd.read_csv(file_path, na_values=miss_value, encoding='utf-8')
data.head()
data.info()
data.describe()

# 计算各个区的面积与单价的相关性
area_set = set(data['所在区域'].values.tolist())
corr_dict = {}

for i in area_set:
    subset = data[data['所在区域'] == i]
    cor = round(subset['建筑面积'].corr(subset['单价']), 2)
    print(i, cor)
    corr_dict[i] = cor

# 计算总体的相关性
overall_corr = round(data['建筑面积'].corr(data['单价']), 2)
print('总体相关性:', overall_corr)

areas = data["建筑面积"]
prices = data["单价"]
# data[data['所在区域']=='延庆']['建筑面积']
# data[data['所在区域']=='延庆']['单价']

# 创建DataFrame
data = pd.DataFrame({
    '面积': areas,
    '单价': prices
})

# 定义面积区间
bin_size = 10  # 每10平米为一个区间
max_area = data['面积'].max()
bins = list(range(0, int(max_area) + bin_size, bin_size))

# 为每个房屋分配所属的区间
data['面积区间'] = pd.cut(data['面积'], bins=bins, right=False)
'''
# 计算每个区间的房子数量
grouped_data_count = data.groupby('面积区间').size().reset_index(name='数量')
# print(grouped_data_count)'''
# 计算每个区间的平均单价和房子数量
grouped_data = data.groupby('面积区间')['单价'].agg(['mean', 'count']).reset_index()

# 提取区间中点作为x坐标
grouped_data['区间中点'] = grouped_data['面积区间'].apply(lambda x: (x.left + x.right) / 2)
grouped_data.columns = ['面积区间', '单价', '数量', '区间中点']
#print(grouped_data)

# 准备数据
x_data = grouped_data['区间中点'].tolist()
y_data = grouped_data['单价'].divide(10000).tolist()
size_data = grouped_data['数量'].tolist()

# 创建数据点列表，每个点包含[x坐标, y坐标, 大小]
data_points = []
for i in range(len(x_data)):
    data_points.append([x_data[i], y_data[i], size_data[i]])

# 使用pyecharts创建散点图
scatter = (
    Scatter(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1500px", height="800px"))
    .add_xaxis([])
    .add_yaxis(
        "平均单价",
        data_points,
        symbol_size=12,
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="房屋面积与单价关系散点图", subtitle="按10平米区间分组"),
        xaxis_opts=opts.AxisOpts(
            type_="value",
            name="房屋面积 (平米)",
            name_location="center",
            name_gap=30,
            min_=0,
            axislabel_opts=opts.LabelOpts(formatter="{value} "),
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name="平均单价 (万元/平米)",
            name_location="center",
            name_gap=40,
            axislabel_opts=opts.LabelOpts(formatter="{value} "),
        ),
        visualmap_opts=opts.VisualMapOpts(
            type_="size",
            min_=min(size_data),
            max_=max(size_data),
            dimension=2,  # 使用第三个维度(索引2)作为视觉映射的依据
            range_size=[15, 70],
            is_show=True,
            pos_right="5%",
            range_text=["多", "少"],
        ),
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger_on='mousemove|click', axis_pointer_type='cross',
            # JScode里面不是注释，有用的，别动
            formatter=JsCode(
                """function(params){
                    return '平均单价:'+params.data[1]+'<br/>'+'区间内房源数:'+params.data[2]
                }
                """
            )
        ),
    )
)

# 生成HTML文件
scatter.render("picture/{}房屋面积单价散点图.html".format(chengshi))

