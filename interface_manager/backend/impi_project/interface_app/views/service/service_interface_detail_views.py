from django.forms.models import model_to_dict
from interface_app import common
from interface_app.models.interface import Interface

from django.views.generic import View
from interface_app.my_exception import MyException

#获取某个服务下的interface列表
class ServiceInterfaceDetailViews(View):
    def get(self,request,pk,*args,**kwargs):
        interfaces = Interface.objects.filter(service_id=pk)
        ret = [model_to_dict(i) for i in interfaces]
        return common.response_success(model_to_dict(ret))
