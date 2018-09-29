####添加登录功能<br>
1、登录视图：<br>
```
def login_action(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "" or password == "":
            return render(request, 'user_app/index.html', {'error': '用户名或密码不能为空！'})

        else:
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return render(request,'user_app/project_manage.html')
            else:
                return render(request,'user_app/index.html',{'error': '用户名或密码错误！'})

```

2、创建管理员账号
```
python manage.py createsuperuser
```
登录管理员账号并添加其他账号，在登录页面使用管理员账号和添加的账号登录

3、修改时区和语言<br>
在settings.py文件中：
```
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
```

4、引用登录模板<br>
1）[引用bootstrap登录模板](https://getbootstrap.com/docs/4.1/examples/sign-in/)
```
<link href="https://getbootstrap.com/docs/4.1/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://getbootstrap.com/docs/4.1/examples/sign-in/signin.css" rel="stylesheet">
```
2）引用本地样式<br>
（1）在manage.py文件统计目录下创建static/css文件夹，在static/css文件夹下创建bootstrap.min.css、signin.css文件（文件内容为格式化引用的模板中的源码）
（2）在settings.py文件下添加如下内容：<br>
```
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
```
（3）在index.html中，去掉引用的bootstrap模板，添加如下内容：<br>
```
{% load static %}
<link rel="stylesheet" type="text/css" href="{% static "css/bootstrap.min.css" %}">
<link rel="stylesheet" type="text/css" href="{% static "css/signin.css" %}">
```

