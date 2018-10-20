1、在project_app文件中新建views文件夹<br>
（1）将原views.py重命名为project_views.py，并将该文件移动到views文件夹中；<br>
（2）在views文件夹中新建module_views.py文件

2、对于project_app中的forms.py
```
from django import forms
from .models import Project,Module

'''
class ProjectForm(forms.Form):
    name = forms.CharField(label="名称",max_length=100)
    describe = forms.CharField(label="描述",widget=forms.Textarea)
    status = forms.BooleanField(label="状态")
'''

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name','describe','status']
        #exclude = ['create_time']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        #fields = ['name','describe','status']
        exclude = ['create_time']
```

3、project_app中urls.py中添加模块管理url:
```
from django.urls import path
from project_app.views import project_views
from project_app.views import module_views
urlpatterns = [
    #项目管理
    path('project_manage/',project_views.project_manage),
    path('add_project/',project_views.add_project),
    path('edit_project/<int:pid>/',project_views.edit_project),
    path('delete_project/<int:pid>/',project_views.delete_project),

    #模块管理
    path('module_manage/',module_views.module_manage),
    path('add_module/',module_views.add_module),
    path('edit_module/<int:mid>/',module_views.edit_module),
    path('delete_module/<int:mid>/',module_views.delete_module),
]
```

4、module_views.py
```
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project_app.models import Module
from django.http import HttpResponseRedirect
from project_app.forms import ModuleForm

# Create your views here.
@login_required
def module_manage(request):
    """模块列表管理"""
    #username = request.COOKIES.get('user','')  #读取浏览器cookie
    username = request.session.get('user','')   #读取浏览器session
    module_all = Module.objects.all()
    return render(request, "module_manage.html",{"user":username,"modules":module_all,"type":"list"})

@login_required
def add_module(request):
    """添加模块"""
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            project = form.cleaned_data['project']
            Module.objects.create(name=name,describe=describe,project=project)

            return HttpResponseRedirect('/manage/module_manage/')
    else:
        form = ModuleForm()

    return render(request,"module_manage.html",{'form':form,'type':'add'})

@login_required
def edit_module(request,mid):
    """编辑模块"""
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            model = Module.objects.get(id=mid)
            model.name = form.cleaned_data['name']
            model.describe = form.cleaned_data['describe']
            model.project = form.cleaned_data['project']
            model.save()
            return HttpResponseRedirect('/manage/module_manage/')
    else:
        if mid:
            form = ModuleForm(instance=Module.objects.get(id=mid))

    return render(request, "module_manage.html", {'form': form, 'type': 'edit'})

@login_required
def delete_module(request,mid):
    """删除模块"""
    Module.objects.get(id=mid).delete()
    return HttpResponseRedirect('/manage/module_manage/')
```


5、新建module_manage.html文件
```
{% extends "base.html" %}
{% block content %}

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed"  data-toggle="collapse" data-target="#navbar"
                  aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">测试平台</a>
        </div>

        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
            <li><a href="#">{{ user }}</a></li>
            <li><a href="/logout">退出</a></li>
          </ul>
          <form class="navbar-form navbar-right">
            <input type="text" class="form-control" placeholder="Search...">
          </form>
        </div>
      </div>
    </nav>

    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar">
            <li><a href="/manage/project_manage/">项目管理</a></li>
            <li class="active"><a href="#">模块管理</a></li>
          </ul>
          <ul class="nav nav-sidebar">
            <li><a href="">用例管理</a></li>
            <li><a href="">任务管理</a></li>
          </ul>
          <ul class="nav nav-sidebar">
            <li><a href="">mockserver</a></li>
            <li><a href="">测试工具</a></li>
          </ul>
        </div>

        {% if type == 'list' %}
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h3 class="sub-header">模块列表
            <button type="button" class="btn btn-default"
                    style="float: right;"
                    onclick="window.location.href='/manage/add_module/'">创建</button>
          </h3>
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>id</th>
                  <th>名称</th>
                  <th>描述</th>
                  <th>项目</th>
                  <th>创建时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {% for module in modules %}
                <tr>
                  <td>{{ module.id }}</td>
                  <td>{{ module.name }}</td>
                  <td>{{ module.describe }}</td>
                  <td>{{ module.project }}</td>
                  <td>{{ module.create_time }}</td>
                  <td>
                      <a href="/manage/edit_module/{{ module.id }}/">编辑</a>
                      <a href="/manage/delete_module/{{ module.id }}/">删除</a>
                  </td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
        {% endif %}

        {% if type == 'add' %}
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h3 class="sub-header">添加模块</h3>
            <div class="table-responsive">
                <form action="/manage/add_module/" method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-default"
                        onclick="window.location.href='/manage/module_manage/'"
                        style="margin-right: 10px;">取消</button>
                    <button type="submit" class="btn btn-success">提交</button>
                </form>
            </div>
        </div>
        {% endif %}

        {% if type == 'edit' %}
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h3 class="sub-header">编辑模块</h3>
          <div class="table-responsive">
            <form role="form" method="post">
                {% csrf_token %}
                {{ form.as_p }}
                <button type="submit" class="btn btn-default"
                    onclick="window.location.href='/manage/module_manage/'"
                    style="margin-right: 10px;">取消</button>
                <button type="submit" class="btn btn-success">保存</button>
            </form>
          </div>
        </div>
        {% endif %}

      </div>
    </div>

{% endblock %}
```