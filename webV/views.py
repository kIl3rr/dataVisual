from django.shortcuts import render
from pyecharts import options as opts
from pyecharts.charts import *
from .models import *
from django.template import loader
from django.http import HttpResponse,FileResponse
import os
from django.urls import reverse

def totalthreeyearsv(request):
    #https://www.dgrt.cn/a/1785818.html?action=onClick
    def geo_formatter(params):return params.name + ' : ' + params.value[2]

    # 定义点击事件处理函数
    # def on_click():
    #     # 获取点击的省份名称
    #     province = params["name"]
    #     if province in ['广东', '山西', '浙江']:
    #         webbrowser.open('https://www.baidu.com')
    years = [2019, 2020, 2021]  # 可选的年份
    data_types = {
        'graduates': '毕业生',
        'entrants': '新生'
    }  # 数据类型选项
    sex_types = {
        'man': '男性',
        'female': '女性',
        '': '空'
    }  # 性别类型选项

    if 'year' in request.GET:
        selected_year = int(request.GET['year'])  # 获取选中的年份
    else:
        selected_year = years[0]  # 默认选择第一个年份

    if 'data_type' in request.GET:
        selected_data_type = request.GET['data_type']  # 获取选中的数据类型
    else:
        selected_data_type = 'graduates'  # 默认选择毕业生

    if 'sex' in request.GET:
        selected_sex = request.GET['sex']  # 获取选中的性别类型
    else:
        selected_sex = ''  # 默认选择空值

    data = totalthreeyears.objects.filter(year=selected_year)  # 根据选中的年份获取数据

    if selected_sex:
        sex_field = selected_data_type + selected_sex
        values = [getattr(d, sex_field) for d in data]  # 根据性别字段获取相应的值
    else:
        values = [getattr(d, selected_data_type) for d in data]  # 根据数据类型获取相应的值

    title = data_types[selected_data_type] + ' in ' + str(selected_year)
    regions = [d.region for d in data]

    if selected_data_type == 'graduates':
        data_range = [0, max(values)]
        data_pieces = [
            {"min": 30000, "label": ">30000", "color": "#4f070d"},
            {"min": 10000, "max": 30000, "label": "10000-30000", "color": "#9c141b"},
            {"min": 8000, "max": 10000, "label": "8000-10000", "color": "#d9272c"},
            {"min": 5000, "max": 8000, "label": "5000-8000", "color": "#ed3237"},
            {"min": 2000, "max": 5000, "label": "2000-5000", "color": "#f2705f"},
            {"max": 2000, "label": "<2000", "color": "#f5bba7"},
        ]
    else:
        data_range = [0, max(values)]
        data_pieces = [
            {"min": 10000, "label": ">10000", "color": "#4f070d"},
            {"min": 5000, "max": 10000, "label": "5000-10000", "color": "#9c141b"},
            {"min": 1000, "max": 4999, "label": "1000-4999", "color": "#d9272c"},
            {"min": 500, "max": 999, "label": "500-999", "color": "#ed3237"},
            {"min": 100, "max": 499, "label": "100-499", "color": "#f2705f"},
            {"max": 99, "label": "<100", "color": "#f5bba7"},
        ]

    # 创建地图
    geo_chart = (
        Geo()
        .add_schema(maptype="china").add("所选省份", [("广东", 1), ("山西", 1), ("浙江", 1)], type_="effectScatter")
        .add(
            series_name=data_types[selected_data_type],
            data_pair=[list(z) for z in zip(regions, values)],
            type_="scatter",
            label_opts=opts.LabelOpts(position="inside"),
            tooltip_opts=opts.TooltipOpts(
                formatter=geo_formatter
            ),  # 小圆点上不出现经纬度
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            
            title_opts=opts.TitleOpts(title=title),
            visualmap_opts=opts.VisualMapOpts(
                min_=data_range[0],
                max_=data_range[1],
                is_piecewise=False,
                pieces=data_pieces,
            )
            # ,tooltip_opts=opts.TooltipOpts(trigger_on=on_click)
        )
    )

    # geo_chart.on("click",on_click)
    # 渲染页面
    chart = geo_chart.render_embed()
    return render(
        request,
        'totalthreeyearsv.html',
        {
            'chart': chart,
            'years': years,
            'selected_year': selected_year,
            'data_types': data_types,
            'selected_data_type': selected_data_type,
            'sex_types': sex_types,
            'selected_sex': selected_sex,
        },
    )


def topprovinceratev(request):
    years = [2019, 2020, 2021]

    if 'year' in request.GET:
        selected_year = int(request.GET['year'])  # 获取选中的年份
    else:
        selected_year = years[0]  # 默认选择第一个年份

    data = topprovincerate.objects.filter(year=selected_year)
    provinces = [d.province for d in data]
    rates = [float(d.rate) for d in data]

    title = "报录比：" + str(selected_year)

    pie_chart = (
        Pie()
        .add(
            series_name=title,
            data_pair=list(zip(provinces, rates)),
            # rosetype="radius",
            radius="55%",
            label_opts=opts.LabelOpts(formatter="{b}: {c}",is_show=True),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国考研报名人数前十名省份的报录比"),
            legend_opts=opts.LegendOpts(is_show=False),  # 隐藏图例
        )
        .set_series_opts(legend_opts=opts.LegendOpts(is_show=False))  # 隐藏图例
    )

    chart = pie_chart.render_embed()
    return render(
        request,
        'topprovinceratev.html',
        {
            'chart': chart,
            'years': years,
            'selected_year': selected_year,
        },
    )


def hotmajorv(request):
    data = classthreeyears.objects.all()

    # 获取所有科目
    subjects = data.values_list('subject', flat=True).distinct()

    # 存储每个科目的 entrants 和 graduates 数据
    entrants_data = {}
    graduates_data = {}

    subs = ['philosophy', 'economics', 'law', 'education', 'literature', 'history', 'science', 'engineering', 'agriculture', 'medicine', 'militaryscience', 'management', 'art']

    # 处理数据
    for subject in subjects:
        subject_data = data.filter(subject=subject).order_by('year')

        # 获取三年的 entrants 和 graduates 数据
        entrants = subject_data.values_list('entrants', flat=True)
        graduates = subject_data.values_list('graduates', flat=True)

        entrants_data[subject] = list(entrants)
        graduates_data[subject] = list(graduates)

    # 筛选出top10的subs
    # ['engineering', 'management', 'medicine', 'science', 'education', 'law', 'agriculture', 'economics', 'literature', 'art']
    top10_subs = sorted(entrants_data, key=lambda x: sum(int(i) for i in entrants_data[x]), reverse=True)[:10]
    # 创建一个 Bar 实例
    bar_chart = Bar()

    # 添加 x 轴数据
    bar_chart.add_xaxis(['Year 1', 'Year 2', 'Year 3'])

    # 添加每个科目的 entrants 数据
    for subject in top10_subs:
        bar_chart.add_yaxis(subject, entrants_data[subject][:3],label_opts=opts.LabelOpts(is_show=False))

    # 添加每个科目的 graduates 数据
    for subject in top10_subs:
        bar_chart.add_yaxis(subject, graduates_data[subject][:3],label_opts=opts.LabelOpts(is_show=False))

    # 设置图表标题和坐标轴名称
    bar_chart.set_global_opts(
        title_opts=opts.TitleOpts(title="热门专业授予学位数和毕业生数"),
        xaxis_opts=opts.AxisOpts(name="Year"),
        yaxis_opts=opts.AxisOpts(name="Number of Students"),
        legend_opts=opts.LegendOpts(pos_right="right")
    )
    return HttpResponse(bar_chart.render_embed())


def hotmajorvv(request):
    data = classthreeyears.objects.all()

    # 获取所有科目
    subjects = data.values_list('subject', flat=True).distinct()

    # 存储每个科目的 entrants 和 graduates 数据
    entrants_data = {}
    graduates_data = {}

    subs = ['philosophy', 'economics', 'law', 'education', 'literature', 'history', 'science', 'engineering', 'agriculture', 'medicine', 'militaryscience', 'management', 'art']

    # 处理数据
    for subject in subjects:
        subject_data = data.filter(subject=subject).order_by('year')

        # 获取三年的 entrants 和 graduates 数据
        entrants = subject_data.values_list('entrants', flat=True)
        graduates = subject_data.values_list('graduates', flat=True)

        entrants_data[subject] = list(entrants)
        graduates_data[subject] = list(graduates)

    # 筛选出top10的subs
    # ['engineering', 'management', 'medicine', 'science', 'education', 'law', 'agriculture', 'economics', 'literature', 'art']
    top10_subs = sorted(entrants_data, key=lambda x: sum(int(i) for i in entrants_data[x]), reverse=True)[:10]

    # 创建折线图对象
    line_chart = Line()

    # 添加x轴数据
    x_data = ['Year 1', 'Year 2', 'Year 3']
    line_chart.add_xaxis(x_data)

    # 添加每个排名前10的科目的折线
    for subject in top10_subs:
        # 计算每年的 entrants/graduates 比例
        ratios = [float(entrants_data[subject][i]) / float(graduates_data[subject][i]) for i in range(3)]

        line_chart.add_yaxis(
            series_name=subject,
            y_axis=ratios,
            symbol="circle",
            symbol_size=6,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )

    # 设置图例位置为左边
    line_chart.set_global_opts(
        title_opts=opts.TitleOpts(title="热门专业入学生/毕业生比例"),
        legend_opts=opts.LegendOpts(pos_bottom='right'),
        xaxis_opts=opts.AxisOpts(name="Year"),
        yaxis_opts=opts.AxisOpts(name="Entrants/Graduates Ratio", min_=1, max_=2),
    )

    return HttpResponse(line_chart.render_embed())


def kyhotwc(request):
    # image_path = '/workspace/dataVz/dataVisual/webV/static/1.png'
    return render(request, 'kyhotsearch.html')

def school(request):
    #https://www.dgrt.cn/a/1785818.html?action=onClick
    def geo_formatter(params):return params.name + ' : ' + params.value[2]
    
    years = [2020, 2021, 2022]  # 可选的年份
    data_types = {
        'rate': '报录比',
        'p': '推免生人数'
    }  # 数据类型选项

    if 'year' in request.GET:
        selected_year = int(request.GET['year'])  # 获取选中的年份
    else:
        selected_year = years[0]  # 默认选择第一个年份

    if 'data_type' in request.GET:
        selected_data_type = request.GET['data_type']  # 获取选中的数据类型
    else:
        selected_data_type = 'rate'  # 默认选择报录比


    data1 = jn.objects.filter(year=selected_year)  # 根据选中的年份获取数据
    data2 = zb.objects.filter(year=selected_year)

    def ret(r):
        applicant = int([getattr(d, "applicants") for d in r][0])
        enrollment = int([getattr(d, "enrollment") for d in r][0])
        tm = int([getattr(d, "tm") for d in r][0])
        rate = applicant/enrollment
        return applicant,enrollment,tm,rate
        
    title ="暨南大学 & 中北大学——" + data_types[selected_data_type] + ' in ' + str(selected_year)

    applicant1,enrollment1,tm1,rate1=ret(data1)
    applicant2,enrollment2,tm2,rate2=ret(data2)

    
    if selected_data_type=="rate":
        fin = [("广东",rate1),("山西",rate2)]
        
    else:
        fin= [("广东",tm1),("山西",tm2)]
  
    # 创建地图
    geo_chart = (
        Geo()
        .add_schema(maptype="china")
        .add(
            series_name=data_types[selected_data_type],
            data_pair=fin,
            type_="effectScatter",
            label_opts=opts.LabelOpts(position="inside"),
            tooltip_opts=opts.TooltipOpts(
                formatter=geo_formatter
            ),  # 小圆点上不出现经纬度
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )

    if selected_data_type=="rate":
        geo_chart.set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            visualmap_opts=opts.VisualMapOpts(
            is_piecewise=False,  
            min_=0,
            max_=8
            )
            # ,tooltip_opts=opts.TooltipOpts(trigger_on=on_click)
        )
        
    else:
        geo_chart.set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            visualmap_opts=opts.VisualMapOpts(
            is_piecewise=False,  
            min_=1000,
            max_=0
            )
            # ,tooltip_opts=opts.TooltipOpts(trigger_on=on_click)
        )


    # geo_chart.on("click",on_click)
    # 渲染页面
    chart = geo_chart.render_embed()
    return render(
        request,
        'schoolthreeyears.html',
        {
            'chart': chart,
            'years': years,
            'selected_year': selected_year,
            'data_types': data_types,
            'selected_data_type': selected_data_type,
        },
    )


def itkyhotwc(request):
    return render(request, 'itkyhotsearch.html')

def index(request):
    link_routes = {
    'totalthreeyearsv': 'Total Three Years',
    'topprovinceratev': 'Top Province Rate',
    'hotmajorv': 'Hot Major',
    'hotmajorvv': 'Hot Major 2',
    'kyhotwc': 'KY Hot WC',
    'school': 'School',
    'itkyhotwc': 'IT KY Hot WC'
    }

    return render(request,'index.html',{'link_routes': link_routes})
