import json
from django.views.generic import View
from interface_app import common
from interface_app.form.debug import DebugForm

from interface_app.my_exception import MyException
from interface_app.utils.interface_utils import InterfaceUtils

#调试功能的接口
class DebugListViews(View):
    """获取全部接口列表"""

    def post(self,request,*args,**kwargs):
        """创建接口"""
        body = request.body
        # print(body)
        params = json.loads(body)
        form = DebugForm(params)
        result = form.is_valid()
        if result:
            # print(form.cleaned_data)
            # interface = Interface.objects.create(**form.cleaned_data)
            #
            # if interface:
            #     return common.response_success()
            # else:
            #     raise MyException("创建失败")
            url = form.cleaned_data["url"]
            method = form.cleaned_data["method"]
            header = form.cleaned_data["header"]
            parameter = form.cleaned_data["parameter"]
            parameter_type = form.cleaned_data["parameter_type"]
            ret = InterfaceUtils.send_request(url,method,header,parameter,parameter_type)
            # ret = InterfaceUtils.send_request(**form.cleaned_data)
            return common.response_success(ret)
        else:
            print(form.errors.as_json())
            return common.response_failed()