import json
from django.forms.models import model_to_dict
from interface_app import common
from interface_app.models.task import Task,TaskInterface
from interface_app.models.interface import Interface
from interface_app.utils.task_utils import TaskUtils

from django.views.generic import View
from interface_app.my_exception import MyException

#task的接口的增删改查
class TaskDetailInterfacesViews(View):
    def get(self,request,pk,*args,**kwargs):
        """
        获取单个任务的接口列表
        :param request
        :param pk:任务的id
        :param args
        :param kwargs
        :return
        """
        results = TaskInterface.objects.filter(task_id=pk)
        last_result = TaskUtils.get_last_result(pk)
        ret = []
        for i in results:
            tmp = model_to_dict(i.interface)
            tmp["task_interface_id"] = i.id
            r = "无"
            if last_result is not None:
                r = TaskUtils.get_last_interface_result(last_result.id,i.interface_id)
            tmp["result"] = r
            ret.append(tmp)
        return common.response_success(ret)

    def post(self,request,pk,*args,**kwargs):
        """
        单个任务增加接口
        {
            "interfaces":[1,2,3,4]
        }
        :param request
        :param pk:任务的id
        :param args
        :param kwargs
        :return
        """
        body = request.body
        params = json.loads(body)
        interfaces = params.get('interfaces',[])
        if not isinstance(interfaces,list):
            raise MyException()

        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            raise MyException("任务不存在")

        for i in interfaces:
            try:
                Interface.objects.get(id=i)
            except Interface.DoesNotExist:
                raise MyException("接口不存在")
            TaskInterface.objects.create(task_id=task.id,interface_id=i)
        return common.response_success()

    def delete(self,request,pk,*args,**kwargs):
        """
        {
            task_interface_id:1,
        }
        任务移除接口
        :param request
        :param pk:task的id
        :param args
        :param kwargs
        :return
        """
        body = request.body
        params = json.loads(body)
        task_interface_id = params.get('task_interface_id', None)
        if task_interface_id is None:
            raise MyException()
        TaskInterface.objects.filter(id=task_interface_id).delete()
        return common.response_success()