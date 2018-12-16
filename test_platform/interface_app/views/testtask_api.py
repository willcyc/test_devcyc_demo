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