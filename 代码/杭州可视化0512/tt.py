from pyecharts import options as opts
from pyecharts.charts import Scatter
from pyecharts.commons.utils import JsCode

class darwToHtml:
    def scatter_charts(self,xlist, ylist):
        scatter = Scatter()
        scatter.add_xaxis(xaxis_data=xlist )
        scatter.add_yaxis(series_name="", y_axis=ylist, label_opts=opts.LabelOpts(is_show=False))
        scatter.set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="value",
                name='x轴'
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name='y轴'
            ),
            title_opts=opts.TitleOpts(title='计算机组成签到图', pos_top='30px', pos_left='center'),
            tooltip_opts=opts.TooltipOpts(is_show=True,trigger_on='mousemove|click',axis_pointer_type='cross',formatter=JsCode(
                """function(params){
                    return '学号:'+params.data[2]+'<br/>'+'姓名:'+params.data[3]
                }
                """
            ))
        )
        return scatter

if __name__:
    dh = darwToHtml()
    xlist = [1.2, 2.3, 2.4, 3.5, 4.6, 5.1]
    ylist = [[2.2,20185476,"xx1"], [2.5,20185475,"xx2"], [1.7,20185474,"xx3"], [4.6,20185473,"xx4"], [5.8,20185472,"xx5"], [6.9,20185470,"xx6"]]
    scatter = dh.scatter_charts(xlist,ylist)
    scatter.render('scatter.html')
