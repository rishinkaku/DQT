#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path

from BaseInfo.views import base_info, get_linked_co, get_district, get_pro_type, query_by_id, add, edit, \
    fake_delete, import_excel, export_excel, recent_top_ten_pro

urlpatterns = [
    # =================  渲染模板  ====================== #
    path('base_info', base_info, name='view_base_info'),
    # ================= AJAX列表 ====================== #
    path('linked_co', get_linked_co),
    path('district', get_district),
    path('pro_type', get_pro_type),
    path('get_top_10_pro', recent_top_ten_pro),
    # =================   CRUD  ====================== #
    path('all', base_info),  # 分页查询
    path('get_by_id/<int:id>', query_by_id),  # 通过ID查询对象
    path('edit/<int:id>', edit),  # 编辑对象
    path('add', add),  # 添加对象
    path('fake_delete', fake_delete),  # 伪删除
    path('import_excel', import_excel),  # 从Excel导入列表
    path('export_excel', export_excel),  # 导出为Excel表格
]
