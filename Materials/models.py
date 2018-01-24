from django.db import models

# Create your models here.
from BaseInfo.models import BaseInfo


class Material(models.Model):
    material_situation = models.AutoField('工程材料情况主键', primary_key=True)
    project = models.ForeignKey(BaseInfo, on_delete=models.CASCADE)
    expected_scale = models.CharField('设计量', max_length=50, blank=True)
    lis_scale = models.CharField('LIS量', max_length=50, blank=True)
    good_arrived_scale = models.CharField('到货量', max_length=50, blank=True)
    memo = models.TextField('备注', blank=True)
    is_del = models.BooleanField('是否删除', default=False)
    create_time = models.DateTimeField('信息创建时间', auto_now_add=True)
    update_time = models.DateTimeField('信息更新时间', auto_now=True)
