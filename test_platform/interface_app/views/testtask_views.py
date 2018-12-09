import os,json
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from interface_app.models import TestTask,TestCase
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from interface_app.extend.task_run import run_cases
from interface_app.apps import TASK_PATH,RUN_TASK_FILE

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
        cases_list = task_obj.cases.split(",")
        cases_list.pop(-1)
        print(cases_list)

        task_obj.status = 1   #修改任务执行状态
        task_obj.save()
        #print(task_obj.cases)

        all_cases_dict = {}
        for case_id in cases_list:
            case_obj = TestCase.objects.get(id=case_id)
            case_dict = {
                "url":case_obj.url,
                "method":case_obj.req_method,
                "type_":case_obj.req_type,
                "header":case_obj.req_header,
                "parameter":case_obj.req_parameter,
                "assert_":case_obj.resp_assert
            }
            all_cases_dict[case_obj.id] = case_dict

        print(all_cases_dict)

        cases_str = json.dumps(all_cases_dict)   #json格式数据转化为字符串
        cases_data_file = TASK_PATH + "cases_data.json"  #用例文件路径
        print(cases_data_file)
        with open(cases_data_file,"w") as f:   #将用例写入到cases_data.json用例文件中
            f.write(cases_str)

        os.system("python " + RUN_TASK_FILE)   #运行用例

        return HttpResponseRedirect("/interface/task_manage/")

    else:
        return HttpResponse("404")

#运行某任务下的用例cases --单元测试框架 + 数据驱动