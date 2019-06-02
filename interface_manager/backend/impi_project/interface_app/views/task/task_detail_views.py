import json
from django.forms.models import model_to_dict
from interface_app import common
from interface_app.form.task import TaskForm
from interface_app.models.task import Task,TaskInterface
from interface_app.models.result import TaskResult

from django.views.generic import View
from interface_app.my_exception import MyException

#task获取、修改或删除接口
class TaskDetailViews(View):
    def get(self,request,pk,*args,**kwargs):
        """获取单个任务"""
        try:
            task = Task.objects.get(id=pk)
            tmp = dict()
            tmp["id"] = task.id
            tmp["name"] = task.name
            tmp["description"] = task.description
            tmp["status"] = task.get_status_display()  # 获取models\task\Task_status表中choice的描述
            tmp["interface_count"] = TaskInterface.objects.filter(task_id=task.id).count()
            tmp["result_count"] = TaskResult.objects.filter(task_id=task.id).count()
        except Task.DoesNotExist:
            return common.response_failed()
        else:
            return common.response_success(tmp)

    def put(self,request,pk,*args,**kwargs):
        """更新单个任务"""
        body = request.body
        params = json.loads(body)
        form = TaskForm(params)  #参数校验
        result = form.is_valid()
        if result:
            Task.objects.filter(id=pk).update(**form.cleaned_data)   #下面形式的简写
            # Service.objects.filter(id=pk).update(name=form.cleaned_data["name"],
            #                                      description=form.cleaned_data["description"],
            #                                      parent=form.cleaned_data["parent"])
        else:
            print(form.errors.as_josn())
            raise MyException()
        return common.response_success()

    def delete(self,request,pk,*args,**kwargs):
        """删除单个任务"""
        Task.objects.filter(id=pk).delete()
        return common.response_success()