#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render


def view_base(request):
    return render(request, 'main.html')
