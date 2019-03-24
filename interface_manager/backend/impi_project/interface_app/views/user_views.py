import json
from django.contrib.sessions.models import Session
#from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from interface_app import common
from interface_app.form.user import UserForm
from django.views.generic import View
from interface_app.my_exception import MyException

class UserViews(View):
    def get(self,request,*args,**kwargs):
        #common.logger.info('Hello logs')
        #raise MyException("这是一主动抛出的异常")
        token = request.META.get("HTTP_TOKEN", None)  # 根据HTTP的head获取token
        if token is None:
            #return common.response_failed("用户未登录！")
            raise MyException("用户未登录！")
        else:
            try:
                session = Session.objects.get(pk=token)  # 获取session的对象
            except Session.DoesNotExist:
                #return common.response_failed("session失效！")
                raise MyException("session失效！")
            # except Exception as e:   #因为有全局异常捕获，且在全局异常捕获里有这个功能，此处可以省略
            #     print(e)
            #     return common.response_failed("未知错误！")
            else:
                user_id = session.get_decoded().get('_auth_user_id', None)  # diango的session固定获取用户的user_id
                if user_id is None:
                    #return common.response_failed("用户id失效！")
                    raise MyException("用户id失效！")
                try:
                    user = User.objects.get(pk=user_id)  # 根据id获取用户
                except User.DoesNotExist:
                    #return common.response_failed("用户不存在！")
                    raise MyException("用户不存在！")
                else:
                    return common.response_success({"username": user.username, "id": user.id})

    def post(self,request,*args,**kwargs):
        body = request.body
        params = json.loads(body)
        form = UserForm(params)
        result = form.is_valid()
        if result:
            # user = User.objects.create_user(username=str(params["username"]), password=str(params["password"]))
            user = User.objects.create_user(username=form.cleaned_data["username"],
                                            password=form.cleaned_data["password"])
            if user:
                login(request, user)  # 表示创建的session
                session = request.session.session_key  # 获取session值
                return common.response_success({"session": session})
            else:
                #return common.response_failed("注册失败！")
                raise MyException("注册失败！")
        else:
            print(form.errors.as_json())
            #return common.response_failed("参数不正确")
            raise MyException()  #my_exception.MyException中默认就是参数错误，所以括号内可以不添加内容

    def put(self,request,*args,**kwargs):
        body = request.body
        params = json.loads(body)
        form = UserForm(params)
        result = form.is_valid()
        if result:
            # user = authenticate(username=params["username"], password=str(params["password"]))
            user = authenticate(username=form.cleaned_data["username"], password=str(form.cleaned_data["password"]))
            if user:
                login(request, user)  # 表示创建的session
                session = request.session.session_key  # 获取session值
                # print("session:",session)
                return common.response_success({"session": session})
            else:
                #return common.response_failed("登录失败！")
                raise MyException("登录失败！")
        else:
            print(form.errors.as_json())
            #return common.response_failed("参数不正确")
            raise MyException()  #my_exception.MyException中默认就是参数错误，所以括号内可以不添加内容

    # def delete(self,request,*args,**kwargs):
    #     return common.response_success({'method': 'delete'})
    #
    # def patch(self,request,*args,**kwargs):
    #     return common.response_success({'method': 'patch'})
