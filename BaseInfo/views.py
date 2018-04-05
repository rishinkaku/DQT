import time
import xlwt
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from functools import reduce

from BaseInfo.forms import BaseInfoForm
from BaseInfo.models import BaseInfo, LinkedCo, District, ProjectType
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import xlrd
import logging
import operator
from os.path import join


#  ========================= CRUD =========================  #

def base_info(request):
    """
    查询所有（is_del为False的）

    1、采用QuerySet加【分片】的方式提高查询性能。QuerySet是惰性的，
    只在对数据库进行求值之后才会对它们执行查询，这比立即查询的
    速度更快。

    2、以后统一采用POST和GET复用的方式，GET主要负责返回页面，
    POST返回数据。

    :param request:
    :return: POST: List BaseInfo, GET: Template baseInfo.html
    """
    if request.method == 'POST':
        page, page_size, conditions = extract_params(request)
        if not page or not page_size:
            return JsonResponse({'mess': '缺少分页参数'})
        start = (page - 1) * page_size
        end = start + page_size
        query = BaseInfo.objects.filter(is_del=False)  # 第一步：查询所有有效条目
        if conditions:  # 第二步：如果有查询条件，在基本查询的基础上继续过滤
            query = query.filter(reduce(operator.or_, conditions))
        #  分页查询优化
        total = query.count()
        query = query[start:end].values('id',
                                        'linked_co__text',
                                        'district__text',
                                        'internal_no',
                                        'pro_type__text',
                                        'pro_no',
                                        'task_code',
                                        'pro_name',
                                        'predict')

        return pagination_handle(request, query, total)
    else:
        # GET请求返回渲染页面
        return render(request, 'BaseInfo/baseInfo.html')


def query_by_id(request, id):
    """
    根据ID查询对象

    当处理单个对象时，用model_to_dict()方法，
    处理对象列表时候参考get_all()
    :param request:
    :param id:
    :return: row: BaseInfo对象
    """
    if request.method == 'GET':
        if id:
            query = BaseInfo.objects.get(pk=id)
            row = model_to_dict(query)
            return JsonResponse(row, safe=False)
        return JsonResponse({'mess': '缺少参数ID'})
    logger.warning('使用了错误的请求方式调用query_by_id')
    return JsonResponse({'mess': '请用GET方式请求'})


def add(request):
    """
    增加对象

    form.error: 表单提交错误原因，有参考意义，
    故直接返回
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = BaseInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'mess': '添加成功！'})
        return JsonResponse({'mess': form.errors})
    return JsonResponse({'mess': '请用POST方式请求'})


def edit(request, id):
    """
    编辑对象

    :param request:
    :param id:
    :return:
    """
    if request.method == 'POST':
        instance = get_object_or_404(BaseInfo, pk=id)
        form = BaseInfoForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return JsonResponse({'mess': '修改成功！'})
    return JsonResponse({'mess': '请用POST方式请求'})


def fake_delete(request):
    """
    批量假删除对象

    :param request:
    :return:
    """
    if request.method == 'GET':
        ids = request.GET.getlist('ids[]')
        if ids:
            rows = BaseInfo.objects.filter(id__in=ids).update(is_del=True)
            if rows > 0:
                return JsonResponse({'mess': '删除成功!'})
            return JsonResponse({'mess': '删除失败!'})
        return JsonResponse({'mess': '缺少参数id/ids'})
    return JsonResponse({'mess': '请用GET方式请求'})


def import_excel(request):
    """
    从Excel导入列表

    :param request:
    :return:
    """
    if request.method == 'POST':
        f = request.FILES['file']
        if f:
            try:
                parse_excel(f)
            except Exception as e:
                print(e)
                return JsonResponse({'mess': '解析Excel出错！'})
            return JsonResponse({'mess': '上传成功!'})
        return JsonResponse({'mess': '上传失败！'})

    return JsonResponse({'mess': '请用POST方式请求'})


def export_excel(request):
    if request.method == 'GET':
        response = HttpResponse(content_type='application/ms-excel')
        t = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        response['Content-Disposition'] = 'attachment; filename="' + t + '.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('sheet1')
        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['序号', '挂靠单位（公司）', '区域', '内部文号', '项目类型', '项目编号', '任务编码', '项目名称',
                   '预计信息点']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        #  这里要做查询限制，后期可用日期条件
        rows = BaseInfo.objects.filter(is_del=False).values_list('id', 'linked_co__text', 'district__text',
                                                                 'internal_no',
                                                                 'pro_type__text', 'pro_no', 'task_code',
                                                                 'pro_name', 'predict')
        for row in rows:
            # row是Tuple，必须转成List才能修改其值
            row = list(row)
            row_num += 1
            # 修改序号
            row[0] = row_num
            # 按照(行坐标,列坐标,样式)依次写入
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        wb.save(response)
        return response


#  ========================= Ajax读取列表 =========================  #
def get_linked_co(request):
    """
    获取挂靠公司列表

    :param request:
    :return:
    """
    query = list(LinkedCo.objects.filter(is_del=False).values())
    return JsonResponse(query, safe=False)


def get_district(request):
    """
    获取区域列表

    :param request:
    :return:
    """
    query = list(District.objects.filter(is_del=False).values())
    return JsonResponse(query, safe=False)


def get_pro_type(request):
    """
    获取项目类型列表

    :param request:
    :return:
    """
    query = list(ProjectType.objects.filter(is_del=False).values())
    return JsonResponse(query, safe=False)


def recent_top_ten_pro(request):
    """
    默认：获取最新的前10的项目
    带参数q: 根据关键字查询最新的前20项目

    字段前的"-"表示按照降序排列
    前端输入框值发生改变后，会发送{"q": 用户输入值}过来，用以检索数据
    :param request:
    :return:
    """
    q = request.POST.get('q')
    if q:
        new_query = list(
            BaseInfo.objects.filter(is_del=False).filter(pro_name__contains=q).order_by('-update_time', '-create_time')[
            :20].values(
                'id',
                'pro_name'))
        return JsonResponse(new_query, safe=False)
    query = list(BaseInfo.objects.all().order_by('-update_time', '-create_time')[:10].values('id', 'pro_name'))
    return JsonResponse(query, safe=False)


#  ========================= 工具函数 =========================  #
def extract_params(request):
    """
    提取分页参数

    后台传过来的条件应为："字段名：值"的列表的形式

    :param request:
    :return: int page, int page_size, list(Q) conditions
    """
    logger = logging.getLogger('django_request')

    try:
        page = int(request.POST.get('page'))
        page_size = int(request.POST.get('rows'))
    except Exception as param_ex:
        logger.warning(param_ex)
        return JsonResponse({'mess': '分页参数不正确'})
    conditions = []
    try:
        field_names = BaseInfo.query_fields()
        condition_name = request.POST.get('name', None)
        if condition_name:
            conditions.append(Q(**{condition_name + '__contains': request.POST.get('value')}))
        # 处理组合查询
        # 代码有问题，但是无法重现请求参数，所以留到需求出现的时候再做修改
        # for name in field_names:
        #     condition_name = request.POST.get('name', None)
        #     if condition_name and condition_name == name:
        #         conditions.append(Q(**{name + '__contains': request.POST.get(name)}))
    except Exception as field_ex:
        logging.warning(field_ex)
    return page, page_size, conditions


def pagination_handle(request, query, total):
    """
    分页处理

    :param request:
    :param query: QuerySet
    :param total: 总条数
    :return: rows: 结果, total: is_del=False的总条数
    """
    page, page_size, conditions = extract_params(request)
    if not page or not page_size:
        return JsonResponse({'mess': '缺少分页参数'})
    paginator = Paginator(query, page_size)
    try:
        query = paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)
    rows = list(query)  # QuerySet --> list
    return JsonResponse({'rows': rows, 'total': total}, safe=False)


def parse_excel(file):
    with open('temp.xls', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    data = xlrd.open_workbook('temp.xls')
    table = data.sheet_by_name(u'汇总表')
    insert_list = []
    for i in range(1, table.nrows):
        row = table.row_values(i)
        b = BaseInfo()
        # 挂靠单位
        for item in LinkedCo.objects.all():
            if item.text == row[1]:
                b.linked_co_id = item.id
                break
        # 区域
        for item in District.objects.all():
            if item.text == row[2]:
                b.district_id = item.id
                break
        # 内部文号
        import random
        if row[3]:
            b.internal_no = row[3]
        else:
            b.internal_no = random.randint(1000, 99999)
        # 项目类型
        b.pro_type_id = 6  # 默认"未知"
        for item in ProjectType.objects.all():
            if item.text == row[4]:
                b.pro_type_id = item.id
                break

        # 项目编号
        b.pro_no = row[5]
        # 任务编码
        b.task_code = row[6]
        # 项目名称
        b.pro_name = row[7]
        # 预计信息点
        b.predict = row[8]
        insert_list.append(b)
    BaseInfo.objects.bulk_create(insert_list)
