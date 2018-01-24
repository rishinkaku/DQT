from django.db import models


class LinkedCo(models.Model):
    """
    挂靠单位
    """
    id = models.AutoField('ID', primary_key=True)
    text = models.CharField('挂靠单位名称', max_length=100)
    memo = models.TextField('备注', blank=True)
    is_del = models.BooleanField('是否删除', default=False)
    create_time = models.DateTimeField('信息创建时间', auto_now_add=True)
    update_time = models.DateTimeField('信息更新时间', auto_now=True)


class District(models.Model):
    """
    区域
    """
    id = models.AutoField('ID', primary_key=True)
    text = models.CharField('区域名称', max_length=100)
    memo = models.TextField('备注', blank=True)
    is_del = models.BooleanField('是否删除', default=False)
    create_time = models.DateTimeField('信息创建时间', auto_now_add=True)
    update_time = models.DateTimeField('信息更新时间', auto_now=True)


class ProjectType(models.Model):
    """
    项目类型
    """
    id = models.AutoField('ID', primary_key=True)
    text = models.CharField('项目类型', max_length=50)
    memo = models.TextField('备注', blank=True)
    is_del = models.BooleanField('是否删除', default=False)
    create_time = models.DateTimeField('信息创建时间', auto_now_add=True)
    update_time = models.DateTimeField('信息更新时间', auto_now=True)


class BaseInfo(models.Model):
    """
    基本信息
    """
    id = models.AutoField('序号', primary_key=True)
    linked_co = models.ForeignKey('LinkedCo', on_delete=models.CASCADE)
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    internal_no = models.CharField('内部文号', max_length=100, unique=True, blank=True)  # 自动生成
    pro_type = models.ForeignKey('ProjectType', on_delete=models.CASCADE)
    pro_no = models.CharField('项目编号', max_length=100, blank=True)
    task_code = models.CharField('任务编码', max_length=100, blank=True)
    pro_name = models.CharField('项目名称', max_length=100)
    predict = models.CharField('预计信息点', max_length=100)
    memo = models.TextField('备注', blank=True, default='')
    is_del = models.BooleanField('是否删除', default=False)
    create_time = models.DateTimeField('信息创建时间', auto_now_add=True)
    update_time = models.DateTimeField('信息更新时间', auto_now=True)

    @staticmethod
    def query_fields():
        """
        :return: list 查询的字段名称
        """
        return ['id', 'internal_no', 'pro_no', 'task_code', 'pro_name', 'predict', 'memo', 'linked_co__text',
                'district__text', 'pro_type__text']
