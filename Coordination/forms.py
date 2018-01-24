#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

from Coordination.models import Coordination


class CoordinationForm(forms.ModelForm):
    class Meta:
        model = Coordination
        fields = '__all__'
