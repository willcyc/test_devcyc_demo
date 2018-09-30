from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

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
                return HttpResponseRedirect("/project_manage/")
                #response.set_cookie('user',username,3600)  #记录浏览器cookie
                #return response
            else:
                return render(request,"index.html",{"error":"用户名或密码错误！"})
    else:
        return render(request,'user_app/index.html')
    
@login_required
def project_manage(request):
    #username = request.COOKIES.get('user','')  #读取浏览器cookie
    username = request.session.get('user','')   #读取浏览器session
    return render(request, "project_manage.html",{"user":username})

def logout(request):
    auth.logout(request)  #清除用户登录状态
    response = HttpResponseRedirect('/')
    return response
