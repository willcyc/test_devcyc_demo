- 修改模板目录templates/ 移动到项目跟目录下面（方便维护）。
- 创建静态文件目录 static/ 引用本地资源文件（不依赖于网络样式）。
- 利用浏览器cookie 记录用户名，并显示在登录成功页面。
- 利用bootstrap 制作登录成功之后的页面，设计主要菜单。
- 添加退出功能

1、修改模板目录templates路径：<br>
（1）将templates文件移动至manage.py统计目录下<br>
（2）在settings.py文件中，替换TEMPLATES下的DIRSvalue值：
```
'DIRS': [os.path.join(BASE_DIR,'templates')],
```

2、引用本地资源文件：<br>
在static目录下，放入下载的css文件（需自行添加signin.css文件）<br>
[Bootstrap样式下载地址](https://github.com/twbs/bootstrap/releases/download/v3.3.7/bootstrap-3.3.7-dist.zip)<br>

3、通过cookie记录用户名、显示在登录成功页面：<br>
在views.py文件中：
```
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
                response = HttpResponseRedirect("/project_manage/")
                response.set_cookie('user',username,3600)  #记录浏览器cookie
                return response
            else:
                return render(request,"index.html",{"error":"用户名或密码错误！"})

@login_required
def project_manage(request):
    username = request.COOKIES.get('user','')  #读取浏览器cookie
return render(request, "project_manage.html",{"user":username})
```

4、通过session记录用户名、显示在登录成功页面：<br>
在views.py文件中：
```
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
            else:
                return render(request,"index.html",{"error":"用户名或密码错误！"})

@login_required
def project_manage(request):
    username = request.session.get('user','')   #读取浏览器session
return render(request, "project_manage.html",{"user":username})
```

5、在url.py文件中添加重定向路径：
```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login_action/',views.login_action),
    path('project_manage/',views.project_manage),
    path('accounts/login/', views.index),  #重定向路径
    path('logout/', views.logout),
]
```

6、引用bootstrap模板设计project_manage.html文件<br>
[引用bootstrap模板](https://v3.bootcss.com/examples/dashboard/)

7、退出功能<br>
在views.py文件中：
```
def logout(request):
    auth.logout(request)  #清除用户登录状态
    response = HttpResponseRedirect('/')
return response
```
