from django.shortcuts import render
#通常是一个包含视图函数的文件或文件夹，用于处理Web应用程序中的请求

# Create your views here.
# views.py

from django.http import JsonResponse
from django.template.backends import django


def add_testcase_return_id(request):
    # 处理请求的逻辑
    django.http(request)
    data = {
        'case_name': 'demo',
        'case_id': 0
    }
    return JsonResponse(data)