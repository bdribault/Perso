#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    path('<str:username>', views.CvView.as_view(), name='cv'),
]
