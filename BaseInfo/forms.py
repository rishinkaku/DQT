#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
注意

留意"ModelForm"和"Form"区别，曾经出现过继承了"Form"而
无法使用模型字段的错误。
"""

from django import forms

from BaseInfo.models import BaseInfo


class BaseInfoForm(forms.ModelForm):
    class Meta:
        model = BaseInfo
        fields = '__all__'
