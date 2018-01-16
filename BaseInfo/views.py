from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from BaseInfo.forms import BaseInfoForm
from BaseInfo.models import BaseInfo, LinkedCo, District, ProjectType
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


#  ========================= 渲染视图 =========================  #
def base_info(request):
    return render(request, 'BaseInfo/baseInfo.html')


#  ========================= CRUD =========================  #
def pagination_handle(request, query):
    """
    分页处理

    :param request: POST
    :param query: QuerySet 查询结果
    :return: rows: 结果, total: is_del=False的总条数
    """
    page, page_size = extract_params(request)
    if not page or not page_size:
        return JsonResponse({'mess': '缺少分页参数'})
    paginator = Paginator(query, page_size)
    total = BaseInfo.objects.filter(is_del=False).count()
    try:
        query = paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)
    rows = list(query)  # QuerySet --> list
    return JsonResponse({'rows': rows, 'total': total}, safe=False)


def get_all(request):
    """
    查询所有（is_del为False的）

    采用QuerySet加分片的方式提高查询性能。QuerySet是惰性的，
    只在对数据库进行求值之后才会对它们执行查询，这比立即查询的
    速度更快。
    :param request: POST
    :return: Json 分页处理后的结果
    """
    if request.method == 'POST':
        page, page_size = extract_params(request)
        if not page or not page_size:
            return JsonResponse({'mess': '缺少分页参数'})
        start = (page - 1) * page_size
        end = start + page_size
        query = BaseInfo.objects.filter(is_del=False)[start:end].values('id', 'linked_co__text', 'district__text',
                                                                        'internal_no',
                                                                        'pro_type__text', 'pro_no', 'task_code',
                                                                        'pro_name',
                                                                        'predict')
        return pagination_handle(request, query)
    return JsonResponse({'mess': '请用POST方式请求'})


def query_by_id(request, id):
    """
    根据ID查询对象

    当处理单个对象时，用model_to_dict()方法，
    处理对象列表时候参考get_all()
    :param request: POST
    :param id:
    :return: row: BaseInfo对象
    """
    if request.method == 'POST':
        if id:
            query = BaseInfo.objects.get(pk=id)
            row = model_to_dict(query)
            return JsonResponse(row, safe=False)
        return JsonResponse({'mess': '缺少参数ID'})
    return JsonResponse({'mess': '请用POST方式请求'})


def add(request):
    """
    增加对象

    form.error: 表单提交错误原因，有参考意义，
    故直接返回
    :param request: POST
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

    :param request: POST
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

    :param request: GET
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


# def import_excel(request):
#     if request.method == 'POST':
#         form = TrainForm(request.POST, request.FILES)
#         if form.is_valid():
#             name = request.POST.get('name')
#             if name:
#                 return face.save_encoding(name, request.FILES['file'])
#     return JsonResponse({'mess': '上传失败！'})


#  ========================= Ajax读取列表 =========================  #
def get_linked_co(request):
    """
    获取挂靠公司列表

    :param request:
    :return:
    """
    query = list(LinkedCo.objects.all().values())
    return JsonResponse(query, safe=False)


def get_district(request):
    """
    获取区域列表

    :param request:
    :return:
    """
    query = list(District.objects.all().values())
    return JsonResponse(query, safe=False)


def get_pro_type(request):
    """
    获取项目类型列表

    :param request:
    :return:
    """
    query = list(ProjectType.objects.all().values())
    return JsonResponse(query, safe=False)


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
