# -*- coding: utf-8 -*-
# @Time    : 2019/1/30 15:33
# @Author  : WANGXIAO
from flask import Blueprint

admin = Blueprint('admin', __name__)

import app.admin.views
