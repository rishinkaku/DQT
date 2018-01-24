#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from os.path import join

from Coordination.forms import CoordinationForm
from Coordination.models import Coordination


def coordination(request):
    """
    查询所有（is_del为False的）

    1、采用QuerySet加【分片】的方式提高查询性能。QuerySet是惰性的，
    只在对数据库进行求值之后才会对它们执行查询，这比立即查询的
    速度更快。

    2、以后统一采用POST和GET复用的方式，GET主要负责返回页面，
    POST返回数据。

    :param request:
    """
    if request.method == 'POST':
        page, page_size = extract_params(request)
        if not page or not page_size:
            return JsonResponse({'mess': '缺少分页参数'})
        start = (page - 1) * page_size
        end = start + page_size
        query = Coordination.objects.filter(is_del=False)[start:end] \
            .values('coordination_id', 'project__pro_name', 'situation', 'construction_paper_paths',
                    'design_material_paths', 'material_usage_paths')
        return pagination_handle(request, query)
    else:
        # GET请求返回渲染页面
        return render(request, 'Coordination/coordination.html')


# def query_by_id(request, id):
#     """
#     根据ID查询对象
#
#     当处理单个对象时，用model_to_dict()方法，
#     处理对象列表时候参考get_all()
#     :param request:
#     :param id:
#     :return: row: BaseInfo对象
#     """
#     if request.method == 'GET':
#         if id:
#             query = Material.objects.get(pk=id)
#             pro_name = query.project.pro_name
#             row = model_to_dict(query)
#             row['project'] = pro_name
#             return JsonResponse(row, safe=False)
#         return JsonResponse({'mess': '缺少参数ID'})
#
#
def add(request):
    """
    增加对象

    form.error: 表单提交错误原因，有参考意义，
    故直接返回
    :param request:
    :return:
    """
    logger = logging.getLogger('django.request')
    if request.method == 'POST':
        try:
            project = request.POST.get('project')
            situation = request.POST.get('situation')
            # 处理多文件上传
            names = ['design_paper_paths', 'construction_paper_paths', 'design_material_paths', 'material_usage_paths']
            files_dic = dict()
            for i in range(len(names)):
                files = request.FILES.getlist(names[i])
                files_path_list = []
                for f in files:
                    destination = open('../DQT/files/coordination' + f.name, 'wb+')
                    for chunk in f.chunks():
                        destination.write(chunk)
                    destination.close()
                    path = str('../DQT/files/coordination' + f.name)
                    files_path_list.append(path)
                files_path_str = ','.join(str(i) for i in files_path_list)
                files_dic[names[i]] = files_path_str
            Coordination(project_id=project, situation=situation, **files_dic).save()
            return JsonResponse({'mess': '添加成功！'})
        except Exception as e1:
            logger.error(e1)
            return JsonResponse({'mess': '添加失败！'})


#
#
# def edit(request, id):
#     """
#     编辑对象
#
#     :param request:
#     :param id:
#     :return:
#     """
#     if request.method == 'POST':
#         instance = get_object_or_404(Material, pk=id)
#         form = MaterialForm(request.POST or None, instance=instance)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'mess': '修改成功！'})
#     return JsonResponse({'mess': '请用POST方式请求'})
#
#
# def fake_delete(request):
#     """
#     批量假删除对象
#
#     :param request:
#     :return:
#     """
#     if request.method == 'GET':
#         ids = request.GET.getlist('ids[]')
#         if ids:
#             rows = Material.objects.filter(material_situation__in=ids).update(is_del=True)
#             if rows > 0:
#                 return JsonResponse({'mess': '删除成功!'})
#             return JsonResponse({'mess': '删除失败!'})
#         return JsonResponse({'mess': '缺少参数id/ids'})
#
#
# #  ========================= Ajax读取列表 =========================  #
# def recent_top_ten_pro(request):
#     """
#     默认：获取最新的前10的项目
#     带参数q: 根据关键字查询最新的前20项目
#
#     字段前的"-"表示按照降序排列
#     前端输入框值发生改变后，会发送{"q": 用户输入值}过来，用以检索数据
#     :param request:
#     :return:
#     """
#     q = request.POST.get('q')
#     if q:
#         new_query = list(
#             BaseInfo.objects.filter(pro_name__contains=q).order_by('-update_time', '-create_time')[:20].values(
#                 'id',
#                 'pro_name'))
#         return JsonResponse(new_query, safe=False)
#     query = list(BaseInfo.objects.all().order_by('-update_time', '-create_time')[:10].values('id', 'pro_name'))
#     return JsonResponse(query, safe=False)
#
#
#  ========================= 工具函数 =========================  #
def extract_params(request):
    """
    提取分页参数

    :param request:
    :return: int page, int page_size
    """
    try:
        page = request.POST.get('page')
        page_size = request.POST.get('rows')
        return int(page), int(page_size)
    except Exception as paramEx:
        print(paramEx)
        return None


def pagination_handle(request, query):
    """
    分页处理

    :param request:
    :param query: QuerySet
    :return: rows: 结果, total: is_del=False的总条数
    """
    page, page_size = extract_params(request)
    if not page or not page_size:
        return JsonResponse({'mess': '缺少分页参数'})
    paginator = Paginator(query, page_size)
    total = Coordination.objects.filter(is_del=False).count()
    try:
        query = paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)
    rows = list(query)  # QuerySet --> list
    return JsonResponse({'rows': rows, 'total': total}, safe=False)
