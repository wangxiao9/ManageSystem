# -*- coding: utf-8 -*-
# @Time    : 2019/1/30 15:35
# @Author  : WANGXIAO

from . import admin


@admin.route('/')
def index():
    return "<h1 style='color:green'>this is flask admin</h1>"
