import traceback
from django.utils.deprecation import MiddlewareMixin
from django.db import DatabaseError
from interface_app.my_exception import MyException
from interface_app.common import response_failed

class MyExceptionMiddleware(MiddlewareMixin):
    def process_request(self,request):
        print("request请求")

    def process_response(self,request,response):
        print("response返回")
        return response

    def process_exception(self,request,exception):   #可以捕获全局异常
        print(traceback.print_exc())  #打印异常
        if isinstance(exception,MyException):
            print("我的错误")
            return response_failed(exception.message)

        elif isinstance(exception,DatabaseError):
            print("数据库错误")
            return response_failed("数据库错误")

        else:
            print("未知错误")
            return response_failed("未知错误")