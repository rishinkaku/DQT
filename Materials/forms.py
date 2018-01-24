#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

from Materials.models import Material


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'
