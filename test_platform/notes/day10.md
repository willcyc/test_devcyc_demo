1、新建interface_app项目
```
python manage.py startproject interface_app
```
（1）将interface_app添加到settings文件中<br>
（2）在test_platform中配置URL，在interface_app中新建urls.py文件<br>

2、用例管理<br>
（1）在interface_app的urls.py文件中添加URL：
```
path('case_manage/',views.case_manage),
```
（2）添加视图<br>
views.py：<br>
```
#用例列表
def case_manage(request):
    if request.method == 'GET':
        return render(request,"case_manage.html",{"type":"list"})
    else:
        return HttpResponse("404")
```

(3)case_manage.html
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
            <li><a href="/manage/module_manage/">模块管理</a></li>
          </ul>
          <ul class="nav nav-sidebar">
            <li class="active"><a href="#">用例管理</a></li>
            <li><a href="/interface/task_manage/">任务管理</a></li>
          </ul>
          <ul class="nav nav-sidebar">
            <li><a href="">mockserver</a></li>
            <li><a href="">测试工具</a></li>
          </ul>
        </div>

        {% if type == 'list' %}
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h3 class="sub-header">用例列表
            <button type="button" class="btn btn-default" id="CreateButton"
                    style="float: right;"
                    onclick="window.location.href='/interface/debug/'">调试</button>
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

      </div>
    </div>

{% endblock %}
```