#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path

from Materials.views import materials, add, fake_delete, query_by_id, edit

urlpatterns = [
    # =================   CRUD  ====================== #
    path('list', materials, name='material_list'),  # 分页查询
    path('add', add),

    path('get_by_id/<int:id>', query_by_id),  # 通过ID查询对象
    path('edit/<int:id>', edit),  # 编辑对象
    path('fake_delete', fake_delete),  # 伪删除
    # path('import_excel', import_excel),  # 从Excel导入列表
    # path('export_excel', export_excel),  # 导出为Excel表格
    # =================   AJAX列表  ====================== #

]
