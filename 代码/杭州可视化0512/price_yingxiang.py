import pandas as pd
from pyecharts.charts import Bar, Line, Grid
from pyecharts import options as opts

name = "hangzhou"
chengshi = "杭州"

file_path = 'E:\\data\\{}\\data_processing\\{}_clean.csv'.format(name, name)
miss_value = ["null", "暂无数据"]
data = pd.read_csv(file_path, na_values=miss_value, encoding='utf-8')
data.head()
data.info()
data.describe()

"""所在区域对房价影响"""
# 各区单价和总价的数据
zone_price = pd.merge(
    data.groupby(['所在区域'])['单价'].mean().round(0).sort_values(ascending=False).to_frame().reset_index(),
    data.groupby(['所在区域'])['总价'].mean().round(0).to_frame().reset_index(),
    on=['所在区域'])

# 各区单价柱状图
bar_danjia = (
    Bar()
    .add_xaxis(zone_price['所在区域'].tolist())
    .add_yaxis("单价(元/平米)", zone_price['单价'].tolist(), z=0)
    .extend_axis(
        yaxis=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} 万元"),interval=130,
                            splitline_opts=opts.SplitLineOpts(is_show=False)
                            )
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="{}各区二手房均价".format(chengshi),
                                  pos_left="center", pos_top="85%", padding=40),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)),
        toolbox_opts=opts.ToolboxOpts(),
    )
)

# 各区总价折线图
line_zongjia = (
    Line()
    .add_xaxis(zone_price['所在区域'].tolist())
    .add_yaxis("总价(万元)", zone_price['总价'].tolist(), yaxis_index=1)
)

bar_danjia.overlap(line_zongjia)  # 将折线图重叠到条形图
bar_danjia.render("picture/{}各区二手房均价.html".format(chengshi))


"""配备电梯对房价影响"""
dianti_price = data.groupby(['配备电梯', '所在区域'])['单价'].agg(['size', 'mean']).round(0).reset_index()
dianti_price.columns = ['配备电梯', '所在区域', '数量', '单价']
#print(dianti_price)

# 有无电梯单价柱状图
bar_dianti = (
    Bar(init_opts=opts.InitOpts(
            # 图表的画布大小  使用的是css格式   px是像素大小
            width='1500px',
            height='800px',
            #page_title='网页标题',
            bg_color='white'# 背景颜色
            )
    )
    .add_xaxis(list(dianti_price[dianti_price['配备电梯'] == '有']['所在区域']))
    .add_yaxis("有电梯", list(dianti_price[dianti_price['配备电梯'] == '有']['单价']), z=0)
    .add_yaxis("无电梯", list(dianti_price[dianti_price['配备电梯'] == '无']['单价']), z=0)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="{}各区有无电梯二手房均价".format(chengshi),
                                  pos_left="center", pos_top="90%", padding=40),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)),
        toolbox_opts=opts.ToolboxOpts(),

    )
    .set_series_opts(
        markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_='average',name='平均值')],
                                        linestyle_opts=opts.LineStyleOpts(type_='dashed' #点状
                                                                          ,opacity=0.9 #透明度 0-1 值越大越不透明
                                                                          #,color='black'
                                        )
        )
    )
)
bar_dianti.render("picture/{}有无电梯二手房价格.html".format(chengshi))

# 有无电梯房源数量
bar_dianti_count = (
    Bar(init_opts=opts.InitOpts(
            # 图表的画布大小  使用的是css格式   px是像素大小
            width='1500px',
            height='800px',
            page_title='网页标题',
            bg_color='white'# 背景颜色
            )
    )
    .add_xaxis(list(dianti_price[dianti_price['配备电梯'] == '有']['所在区域']))
    .add_yaxis("有电梯", list(dianti_price[dianti_price['配备电梯'] == '有']['数量']), stack="电梯堆叠组")
    .add_yaxis("无电梯", list(dianti_price[dianti_price['配备电梯'] == '无']['数量']), stack="电梯堆叠组")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="{}各区有无电梯二手房数量对比".format(chengshi),
                                  pos_left="center", pos_top="90%", padding=40),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)),
        toolbox_opts=opts.ToolboxOpts(),

    )
)
bar_dianti_count.render("picture/{}有无电梯二手房数量.html".format(chengshi))

"""房屋户型对房价影响"""
# 各户型单价和总价的数据
huxing_price = pd.merge(
    data.groupby(['房屋户型'])['单价'].mean().round(0).sort_values(ascending=False).to_frame().reset_index(),
    data.groupby(['房屋户型'])['总价'].mean().round(0).to_frame().reset_index(),
    on=['房屋户型'])
# 只保留数量最多的15种户型
huxing_top_15 = data['房屋户型'].value_counts().head(15).index.tolist()
huxing_top_15_price = huxing_price[huxing_price['房屋户型'].isin(huxing_top_15)]
#print(huxing_top_15_price)
# 各户型单价柱状图
bar_huxing = (
    Bar()
    .add_xaxis(huxing_top_15_price['房屋户型'].tolist())
    .add_yaxis("单价(元/平米)", huxing_top_15_price['单价'].tolist(),z=0)
    .extend_axis(
        yaxis=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} 万元"),interval=300,
                            splitline_opts=opts.SplitLineOpts(is_show=False)
                            )
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="{}各户型二手房均价".format(chengshi)),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0, rotate=45)),
        toolbox_opts=opts.ToolboxOpts(),
    )
)
'''# 各户型总价折线图
line_huxing = (
    Line()
    .add_xaxis(huxing_top_15_price['房屋户型'].tolist())
    .add_yaxis("总价(万元)", huxing_top_15_price['总价'].tolist(), yaxis_index=1)
)
bar_huxing.overlap(line_huxing)  # 将折线图重叠到条形图'''
bar_huxing.render("picture/{}各户型二手房均价.html".format(chengshi))


"""装修情况对房价影响"""
zhuangxiu_price = data.groupby(['装修情况', '所在区域'])['单价'].agg(['size', 'mean']).round(0).reset_index()
zhuangxiu_price.columns = ['装修情况', '所在区域', '数量', '单价']
#print(zhuangxiu_price)

# 精装/简装单价柱状图
bar_zhuangxiu = (
    Bar(init_opts=opts.InitOpts(
            # 图表的画布大小  使用的是css格式   px是像素大小
            width='1500px',
            height='800px',
            #page_title='网页标题',
            bg_color='white'# 背景颜色
            )
    )
    .add_xaxis(list(zhuangxiu_price[zhuangxiu_price['装修情况'] == '精装']['所在区域']))
    .add_yaxis("精装", list(zhuangxiu_price[zhuangxiu_price['装修情况'] == '精装']['单价']), z=0)
    .add_yaxis("简装", list(zhuangxiu_price[zhuangxiu_price['装修情况'] == '简装']['单价']), z=0)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="{}各区精装/简装二手房均价".format(chengshi),
                                  pos_left="center", pos_top="90%", padding=40),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)),
        toolbox_opts=opts.ToolboxOpts(),

    )
    .set_series_opts(
        markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_='average',name='平均值')],
                                        linestyle_opts=opts.LineStyleOpts(type_='dashed' #点状
                                                                          ,opacity=0.9 #透明度 0-1 值越大越不透明
                                                                          #,color='black'
                                        )
        )
    )
)
bar_zhuangxiu.render("picture/{}精装简装二手房价格.html".format(chengshi))

# 精装/简装房源数量
bar_zhuangxiu_count = (
    Bar(init_opts=opts.InitOpts(
            # 图表的画布大小  使用的是css格式   px是像素大小
            width='1500px',
            height='800px',
            page_title='网页标题',
            bg_color='white'# 背景颜色
            )
    )
    .add_xaxis(list(zhuangxiu_price[zhuangxiu_price['装修情况'] == '精装']['所在区域']))
    .add_yaxis("精装", list(zhuangxiu_price[zhuangxiu_price['装修情况'] == '精装']['数量']), stack="堆叠组")
    .add_yaxis("简装", list(zhuangxiu_price[zhuangxiu_price['装修情况'] == '简装']['数量']), stack="堆叠组")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="{}各区精装/简装二手房数量对比".format(chengshi),
                                  pos_left="center", pos_top="90%", padding=40),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)),
        toolbox_opts=opts.ToolboxOpts(),

    )
)
bar_zhuangxiu_count.render("picture/{}精装简装二手房数量.html".format(chengshi))