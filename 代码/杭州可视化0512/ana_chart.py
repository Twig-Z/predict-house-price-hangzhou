import numpy as np
import pandas as pd
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts

name = "hangzhou"
chengshi = "杭州"

"""数据加载"""
file_path = 'E:\\data\\{}\\data_processing\\{}_clean.csv'.format(name, name)


miss_value = ["null", "暂无数据"]
df = pd.read_csv(file_path, na_values=miss_value,encoding="utf-8")
print(df.info())

"""二手房单价最高小区Top10"""
unit_price = pd.merge(
    df.groupby(['小区名称'])['单价'].mean().round(0).sort_values(ascending=False)[:10].to_frame().reset_index(),
    df.groupby(['小区名称'])['总价'].mean().round(0).to_frame().reset_index(),
    on=['小区名称'])
unitprice_top = unit_price.sort_values(by="单价", ascending=False)[:10]
# 使用社区名称作为 x 轴
bar_top10 = (
    Bar()
    .add_xaxis(unit_price["小区名称"].tolist())
    .add_yaxis("单价(元/平米)", unit_price["单价"].tolist(),
               label_opts=opts.LabelOpts(position='inside',formatter='{b}:{c}')
               )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="{}二手房单价最高小区Top10".format(chengshi),
                                  pos_left="center",pos_top="85%",padding=40),

        yaxis_opts=opts.AxisOpts(name="单价(元/平米)",is_show=False),

    )
    .reversal_axis()  # 将x轴和y轴互换，使图表变为横向布局
    #.set_global_opts(datazoom_opts=opts.DataZoomOpts(orient="vertical"))
)
bar_top10.render("picture/{}_top10_price.html".format(name))  # 生成HTML文件

"""二手房单价最高位置Top10"""
pos_price = pd.merge(
    df.groupby(['所在位置'])['单价'].mean().round(0).sort_values(ascending=False)[:10].to_frame().reset_index(),
    df.groupby(['所在位置'])['总价'].mean().round(0).to_frame().reset_index(),
    on=['所在位置'])
posprice_top = pos_price.sort_values(by="单价", ascending=False)[:10]
# 使用社区名称作为 x 轴
bar_top10 = (
    Bar()
    .add_xaxis(posprice_top["所在位置"].tolist())
    .add_yaxis("单价(元/平米)", posprice_top["单价"].tolist(),
               label_opts=opts.LabelOpts(position='inside',formatter='{b}:{c}')
               )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="{}二手房单价最高位置Top10".format(chengshi),
                                  pos_left="center",pos_top="85%",padding=40),

        yaxis_opts=opts.AxisOpts(name="单价(元/平米)",is_show=False),

    )
    .reversal_axis()  # 将x轴和y轴互换，使图表变为横向布局
    #.set_global_opts(datazoom_opts=opts.DataZoomOpts(orient="vertical"))
)
bar_top10.render("picture/{}_top10_pos_price.html".format(name))  # 生成HTML文件

"""二手房房屋户型占比情况"""
count_fwhx = df['房屋户型'].value_counts().head(10)
other_count = df['房屋户型'].value_counts()[10:].sum()
count_other_fwhx = pd.Series({"其他": other_count})
count_fwhx = pd.concat([count_fwhx, count_other_fwhx])
# 准备数据对（类别、频次）
data_pair_fwhx = [[k, v] for k, v in count_fwhx.items()]
pie_fwhx = (
    Pie()
    .add("", data_pair_fwhx, radius=["30%", "75%"])
    .set_global_opts(title_opts=opts.TitleOpts(title="{}二手房房屋户型占比情况".format(chengshi),
                                               pos_left="center",pos_top="85%",padding=40))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
)
pie_fwhx.render("picture/{}_houseType.html".format(name))

"""二手房房屋装修占比情况"""
count_zxqk = df["装修情况"].value_counts()
data_pair_zxqk = [[k, v] for k, v in count_zxqk.items()]
pie_zxqk = (
    Pie()
    .add("", data_pair_zxqk, radius=["30%", "75%"])
    .set_global_opts(title_opts=opts.TitleOpts(title="{}二手房装修占比情况".format(chengshi),
                                               pos_left="center",pos_top="85%",padding=40))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
)
pie_zxqk.render("picture/{}_houseDecoration.html".format(name))

"""二手房建筑类型占比情况"""
count_jzlx = df["建筑类型"].value_counts()
data_pair_jzlx = [[k, v] for k, v in count_jzlx.items()]
pie_jzlx = (
    Pie()
    .add("", data_pair_jzlx, radius=["30%", "75%"])
    .set_global_opts(title_opts=opts.TitleOpts(title="{}二手房建筑类型占比情况".format(chengshi),
                                               pos_left="center",pos_top="85%",padding=40))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
)
pie_jzlx.render("picture/{}_buildType.html".format(name))

"""二手房房屋朝向分布情况"""
count_fwcx = df["房屋朝向"].value_counts()[:15]
count_other_fwcx = pd.Series({"其他": df['房屋朝向'].value_counts()[15:].sum()})
count_fwcx = pd.concat([count_fwcx, count_other_fwcx])
top10_direction = count_fwcx.sort_values(ascending=False).head(10)
bar_fwcx = (
    Bar()
    .add_xaxis(top10_direction.index.tolist())
    .add_yaxis("数量", top10_direction.values.tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title="{}房源朝向分布情况".format(chengshi),
                                  pos_left="center",pos_top="85%",padding=40),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0)
        ))
)
bar_fwcx.render("picture/{}_houseDirection.html".format(name))
