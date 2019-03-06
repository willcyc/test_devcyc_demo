import json
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from interface_app import common

def register_user(request):
    if "POST" == request.method:
       body = request.body
       params = json.loads(body)
       if "name" in params and "" != str(params["name"]) and "pwd" in params and "" != str(params["pwd"]):
           # user = User(username=str(params["name"]),password=str(params["pwd"]))
           # user.save()   该方法的password没有加密、且不能使用一些属性，不如User.objects.create_user()方法

           user = User.objects.create_user(username=str(params["name"]), password=str(params["pwd"]))
           if user:
               login(request, user)   #表示创建的session
               session = request.session.session_key   #获取session值
               return common.response_success({"session":session})
           else:
               return common.response_failed("注册失败！")
       else:
           return common.response_failed("参数不正确")

    else:
        return HttpResponse(status=404)

def login_user(request):
    if "POST" == request.method:
       body = request.body
       params = json.loads(body)
       if "name" in params and ""!=str(params["name"]) and "pwd" in params and ""!=str(params["pwd"]):
           user = authenticate(username=params["name"], password=str(params["pwd"]))
           if user:
                login(request,user)  #表示创建的session
                session = request.session.session_key  # 获取session值
                #print("session:",session)
                return common.response_success({"session": session})
           else:
                return common.response_failed("登录失败！")
       else:
            return common.response_failed("参数不正确")
    else:
        return HttpResponse(status=404)

def get_user(request):
    if "GET" == request.method:
        # user = request.user
        # print("user:",user)
        # if user.is_authenticated:
        #     return common.response_success({"username":user.username,"id":user.id})
        # else:
        #    return common.response_failed("用户未登录！")

        token = request.META.get("HTTP_TOKEN",None)   #根据HTTP的head获取token
        if token is None:
            return common.response_failed("用户未登录！")
        else:
            try:
                session = Session.objects.get(pk=token)  #获取session的对象
            except Session.DoesNotExist:
                return common.response_failed("session失效！")
            except Exception as e:
                print(e)
                return common.response_failed("未知错误！")
            else:
                user_id = session.get_decoded().get('_auth_user_id',None)  #diango的session固定获取用户的user_id
                if user_id is None:
                    return common.response_failed("用户id失效！")
                try:
                    user = User.objects.get(pk=user_id)   #根据id获取用户
                except User.DoesNotExist:
                    return common.response_failed("用户不存在！")
                else:
                    return common.response_success({"username":user.username,"id":user.id})

    else:
        return HttpResponse(status=404)
