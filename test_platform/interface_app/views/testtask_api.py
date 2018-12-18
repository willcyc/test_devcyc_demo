import json
import requests
from test_platform import common
from interface_app.models import TestCase,TestTask,TestResult
from project_app.models import Project, Module

#保存任务
def save_task_data(request):
    if request.method == "POST":
        name = request.POST.get("task_name", "")
        describe = request.POST.get("task_describe", "")
        cases = request.POST.get("task_cases", "")

        print("用例id",cases)
        print(type(cases))

        if name == "":
            return common.response_failed("任务名称不能为空！")

        #保存到数据库
        task = TestTask.objects.create(name=name,describe=describe,cases=cases)
        print(task)
        if task is not None:
            return common.response_succeed(message="创建任务成功!")
        else:
            return common.response_failed("请重新创建任务！")
    else:
        return common.response_failed("请求方法错误！")

#查看任务
def task_result(request):
    if request.method == "POST":
        rid = request.POST.get("result_id", "")
        result_obj = TestResult.objects.get(id=rid)
        data = {
            "result":result_obj.result,
        }
        return common.response_succeed(message="获取成功!",
                                       data=data)
    else:
        return common.response_failed("请求方法错误！")

#获取指定任务信息
def get_task_info(request):
    if request.method == "POST":
        task_id = request.POST.get("taskId","")

        if task_id == "":
            return common.response_failed("任务id为空")

        try:
            task_obj = TestTask.objects.get(pk=task_id)
            task_name = task_obj.name
            task_describe = task_obj.describe
        except TestCase.DoesNotExist:
            return common.response_failed("该任务id不存在！")

        cases_id = task_obj.cases.split(",")
        cases_id.pop(-1)

        tasks_list = []
        for case_id in cases_id:
            case_obj = TestCase.objects.get(id=case_id)
            case_name = case_obj.name

            module_obj = Module.objects.get(name=case_obj.module)
            module_name = module_obj.name

            project_obj = Project.objects.get(name=module_obj.project)
            project_name = project_obj.name
            task_info = project_name + "->" + module_name + "->" + case_name

            tasks_dict = {
                "caseId":case_id,
                "taskInfo":task_info
            }
            tasks_list.append(tasks_dict)
            tasks_info = {
                "taskId":task_id,
                "name": task_name,
                "describe": task_describe,
                "taskList":tasks_list
            }
        print(tasks_info)
        return common.response_succeed(data=tasks_info)
    else:
        return common.response_failed("请求方法错误")

def update_task_data(request):
    if request.method == "POST":
        task_id = request.POST.get("tid", "")
        name = request.POST.get("task_name", "")
        describe = request.POST.get("task_describe", "")
        cases = request.POST.get("task_cases", "")
        print("接口ID：", task_id)

        print("用例id",cases)
        print(type(cases))

        if name == "":
            return common.response_failed("任务名称不能为空！")

        #保存到数据库
        task_obj = TestTask.objects.filter(id=task_id).update(name=name,describe=describe,cases=cases)
        print(task_obj)
        if task_obj == 1:
            return common.response_succeed(message="更新任务成功!")
        else:
            return common.response_failed("请重新创建任务！")
    else:
        return common.response_failed("请求方法错误！")