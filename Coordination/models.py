from django.db import models

from BaseInfo.models import BaseInfo


class Coordination(models.Model):
    coordination_id = models.AutoField('项目协调ID', primary_key=True)
    project = models.ForeignKey(BaseInfo, on_delete=models.CASCADE)
    situation = models.CharField('协调情况', max_length=100, blank=True)
    design_paper_paths = models.TextField('设计图纸文件路径', blank=True)
    construction_paper_paths = models.TextField('施工图纸文件路径', blank=True)
    design_material_paths = models.TextField('设计材料单文件路径', blank=True)
    material_usage_paths = models.TextField('材料使用量文件路径', blank=True)
    memo = models.TextField('备注', blank=True, default='')
    is_del = models.BooleanField('是否删除', default=False)
    create_time = models.DateTimeField('信息创建时间', auto_now_add=True)
    update_time = models.DateTimeField('信息更新时间', auto_now=True)
