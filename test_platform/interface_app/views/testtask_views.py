import os
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from interface_app.models import TestTask
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from interface_app.extend.task_run import run_cases

# Create your views here.

#任务列表
def task_manage(request):
    testtasks = TestTask.objects.all().order_by("id")

    paginator = Paginator(testtasks, 3)  #每页3条数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)  # 如果页数不是整型, 取第一页
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)  #如果页数超出查询范围，取最后一页

    if request.method == 'GET':
        return render(request,"task_manage.html",{"type":"list","testtasks":contacts})
    else:
        return HttpResponse("404")

#创建任务
def add_task(request):
    if request.method == "GET":
        return render(request,"add_task.html",{"type":"add"})
    else:
        return HttpResponse("404")

#运行任务
def run_task(request,tid):
    if request.method == 'GET':
        task_obj = TestTask.objects.get(id=tid)
        #print(task_obj.cases)
        case_list = task_obj.cases.split(",")
        case_list.pop(-1)
        #print(case_list)
        os.system("python D:/git/test_devcyc_demo/test_platform/interface_app/extend/task_run.py") #运行用例

        return HttpResponseRedirect("/interface/task_manage/")

    else:
        return HttpResponse("404")

#运行某任务下的用例cases --单元测试框架 + 数据驱动