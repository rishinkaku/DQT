#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Coordination.views import coordination, add
from django.urls import path

urlpatterns = [
    # =================   CRUD  ====================== #
    path('list', coordination, name='coordination_list'),  # 分页查询
    path('add', add),
    #
    # path('get_by_id/<int:id>', query_by_id),  # 通过ID查询对象
    # path('edit/<int:id>', edit),  # 编辑对象
    # path('fake_delete', fake_delete),  # 伪删除
    # path('import_excel', import_excel),  # 从Excel导入列表
    # path('export_excel', export_excel),  # 导出为Excel表格
    # =================   AJAX列表  ====================== #

]
