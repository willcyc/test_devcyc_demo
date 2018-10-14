from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
#from user_app.models import Project

# Create your views here.
def index(request):
    return render(request,"index.html")

#处理登录
def login_action(request):
    if request.method == "POST":
        username = request.POST.get("username","")
        password = request.POST.get("password","")

        if username == ""  or password == "":
            return render(request, "index.html",{"error":"用户名或密码不能为空"})

        else:   #认证admin/后台的用户
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)   #记录用户登录状态
                request.session['user'] = username
                return HttpResponseRedirect("/manage/project_manage/")
                #response.set_cookie('user',username,3600)  #记录浏览器cookie
                #return response
            else:
                return render(request,"index.html",{"error":"用户名或密码错误！"})
    else:
        return render(request,'index.html')

def logout(request):
    auth.logout(request)  #清除用户登录状态
    response = HttpResponseRedirect('/')
    return response
