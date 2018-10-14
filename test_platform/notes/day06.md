1、创建project_app
```
python manage.py startapp project_app
```
（1）在settings.py文件INSTALLED_APPS中，添加创建的project_app：
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_app.apps.UserAppConfig',
    'project_app.apps.ProjectAppConfig',
]
```

（2）在project_app models.py中创建表单：
```
from django.db import models

# Create your models here.
class Project(models.Model):
    """项目表 """
    name = models.CharField("名称",max_length=100,blank=False,default="")  #https://www.cnblogs.com/ccorz/p/Django-models-zhong-guan-yublank-yunull-de-bu-chon.html
    describe = models.TextField("描述",default="")
    status = models.BooleanField("状态",default=True)
    create_time = models.DateTimeField("创建时间",auto_now=True)

    def __str__(self):
        return self.name

class Module(models.Model):
    """模块表"""
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=100, blank=False, default="")
    describe = models.TextField("描述", default="")
    create_time = models.DateTimeField("创建时间", auto_now=True)

    def __str__(self):
        return self.name
```
（2）在project_app admin.py中：
```
from django.contrib import admin
from project_app.models import Project,Module
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name','describe','status','create_time','id']

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name','describe','create_time','project','id']

admin.site.register(Project,ProjectAdmin)
admin.site.register(Module,ModuleAdmin)
```

（3）创建表单：
```
python manage.py makemigrations
python manage.py migrate
```

（4）在test_platform文件、urls.py中映射project_app文件中的urls：
```
from django.contrib import admin
from django.urls import path,include
from user_app import views
from project_app import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login_action/',views.login_action),
    #path('project_manage/',views.project_manage),
    path('accounts/login/', views.index),
    path('logout/', views.logout),
    path('manage/',include('project_app.urls'))
]
```

（5）在project_app文件中的urls.py文件中：
```
from django.urls import path
from project_app import views

urlpatterns = [
    path('project_manage/',views.project_manage),
    path('add_project/',views.add_project),
]
```

2、重构，修改模板，模板的继承<br>
（1）编写通用模板base.html：
```
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <meta name="description" content="">
    <meta name="author" content="">
    <!--<link rel="icon" href="../../favicon.ico">-->

    <title>测试平台</title>

    <!-- 引用CDN样式 -->
    <!--<link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">-->
    <!--<link href="https://v3.bootcss.com/examples/signin/signin.css" rel="stylesheet">-->
    <!--<link href="https://v3.bootcss.com/examples/dashboard/dashboard.css" rel="stylesheet">-->

    <!--引用本地样式-->
    {% load static %}
    <link rel="stylesheet" type="text/css" href="{% static "css/bootstrap.min.css" %}">
    <link rel="stylesheet" type="text/css" href="{% static "css/signin.css" %}">
    <link rel="stylesheet" type="text/css" href="{% static "css/dashboard.css" %}">

  </head>

  <body>
    {% block content %}{% endblock %}
  </body>

</html>
```

（2）模板的继承<br>
以index.html为例：
```
{% extends "base.html" %}
{% block content %}

    <div class="container">

      <form class="form-signin" method="post" action="/login_action/">
        <h2 class="form-signin-heading">测试平台</h2>
        <label for="inputUsername" class="sr-only">Username</label>
        <input type="text" name="username" id="inputUsername" class="form-control" placeholder="请输入用户名" required>
        <label for="inputPassword" class="sr-only">Password</label>
        <input type="password"  name="password" id="inputPassword" class="form-control" placeholder="请输入密码" required>
          {{ error }}
          {% csrf_token %}
        <div class="checkbox">
          <label>
            <input type="checkbox" value="remember-me"> 记住密码
          </label>
        </div>
        <button class="btn btn-lg btn-primary btn-block" type="submit">登录</button>
      </form>

    </div> <!-- /container -->

{% endblock %}
```

3、创建添加项目表单<br>
（1）project_app urls.py中添加如下内容：
```
path('add_project/',views.add_project)
```
（2）project_app views.py视图中添加add_project：
```
@login_required
def add_project(request):
    """添加项目"""
    return render(request, "project_manage.html",{"type":"add"})
```
（3）project_manage.html：
```
{% if type == 'list' %}
<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
  <h3 class="sub-header">项目列表
    <button type="button" class="btn btn-default"
            style="float: right;"
            onclick="window.location.href='/manage/add_project/'">创建</button>
  </h3>
  <div class="table-responsive">
    <table class="table table-striped">
      <thead>
        <tr>
          <th>id</th>
          <th>名称</th>
          <th>描述</th>
          <th>状态</th>
          <th>创建时间</th>
        </tr>
      </thead>
      <tbody>
        {% for project in projects %}
        <tr>
          <td>{{ project.id }}</td>
          <td>{{ project.name }}</td>
          <td>{{ project.describe }}</td>
          <td>{{ project.status }}</td>
          <td>{{ project.create_time }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endif %}

{% if type == 'add' %}
<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
  <h3 class="sub-header">添加项目</h3>
  <div class="table-responsive">
    创建项目的表单，敬请期待！！！
  </div>
</div>
{% endif %}
```



