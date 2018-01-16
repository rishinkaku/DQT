#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

from BaseInfo.models import BaseInfo


class BaseInfoForm(forms.ModelForm):
    class Meta:
        model = BaseInfo
        fields = '__all__'
