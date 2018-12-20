import json
import requests
from test_platform import common
from interface_app.models import TestCase,TestTask,TestResult
from project_app.models import Project, Module
from interface_app.views.testcase_api import return_cases_list
from interface_app.extend.task_thread import TaskThread

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

        # 去掉最后一个字符
        if cases[-1] == ",":
            cases = cases[:-1]

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

#运行任务
def run_task(request):
    if request.method == "POST":
        tid = request.POST.get("task_id", "")

        if tid == "":
            return common.response_failed("任务id不能为空")

        task_list = TestTask.objects.all()

        running_task = 0
        for task in task_list:
            if task.status == 1:
                running_task = 1;
                break
        if running_task == 1:
            return common.response_failed("当前有任务正在执行...")
        else:
            TaskThread(tid).new_run()
            return common.response_succeed(message="已执行")
    else:
        return common.response_failed("请求方法错误")

#获取指定任务信息
def get_task_info(request):
    if request.method == "POST":
        tid = request.POST.get("taskId","")

        if tid == "":
            return common.response_failed("任务id为空")

        try:
            task_obj = TestTask.objects.get(id=tid)
        except TestTask.DoesNotExist:
            return common.response_failed("该任务id不存在！")

        task_info = {
            "id":task_obj.id,
            "name":task_obj.name,
            "describe":task_obj.describe
        }
        cases_id = task_obj.cases.split(",")
        print("cases_id:",cases_id)

        cases_list = return_cases_list()
        print(cases_list)

        for i in range(len(cases_list)):
            for cid in cases_id:
                if int(cid) == int(cases_list[i]["id"]):
                    cases_list[i]["status"] = True
                    break
                else:
                    cases_list[i]["status"] = False
        task_info["cases"] = cases_list

        return common.response_succeed(message="获取成功！", data=task_info)
    else:
        return common.response_failed("请求方法错误")

#更新任务
def update_task_data(request):
    if request.method == "POST":
        tid = request.POST.get("tid", "")
        name = request.POST.get("task_name", "")
        describe = request.POST.get("task_describe", "")
        cases = request.POST.get("task_cases", "")
        print("接口ID：", tid)

        print("用例id",cases)
        print(type(cases))

        if tid == "":
            return common.response_failed("任务id不能为空！")

        # 去掉最后一个字符
        if cases[-1] == ",":
            cases = cases[:-1]

        task_obj = TestTask.objects.get(id=tid)
        task_obj.name = name
        task_obj.describe = describe
        task_obj.cases = cases
        task_obj.save()

        print(task_obj)

        return common.response_succeed(message="更新任务成功!")

    else:
        return common.response_failed("请求方法错误！")

#删除任务
def delete_task(request):
    if request.method == "POST":
        tid = request.POST.get("task_id", "")
        if tid == "":
            return common.response_failed("任务id不能为空")

        task_obj = TestTask.objects.get(id=tid)
        task_obj.delete()
        return common.response_succeed(message="删除成功！")
    else:
        return common.response_failed("请求方法错误！")