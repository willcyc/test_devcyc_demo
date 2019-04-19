import json
from django.views.generic import View
from interface_app import common


#用于测试的接口
class TestListViews(View):

    def post(self,request,*args,**kwargs):
        """测试的post请求"""
        body = request.body
        #print(body)
        params = json.loads(body)
        test = params.get('test',None)
        print(params)
        if test is not None:
            return common.response_success(params)
        else:
            return common.response_failed()

    def put(self, request, *args, **kwargs):
        """测试的put请求"""
        body = request.body
        params = json.loads(body)
        test = params.get('test', None)
        print(params)
        if test is not None:
            return common.response_success(params)
        else:
            return common.response_failed()

    def delete(self, request, *args, **kwargs):
        """测试的delete请求"""
        body = request.body
        params = json.loads(body)
        test = params.get('test', None)
        print(params)
        if test is not None:
            return common.response_success(params)
        else:
            return common.response_failed()