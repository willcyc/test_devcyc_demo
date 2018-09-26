from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth

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
                auth.login(request, user)
                return render(request,"project_manage.html")
            else:
                return render(request,"index.html",{"error":"用户名或密码错误！"})

        '''
        elif username == "admin" and password == "admin123":
            return render(request, "project_manage.html")
        else:
            return render(request, "index.html", {"error": "用户名或密码错误！"})
        '''