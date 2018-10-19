1、在project_app中创建forms.py表单<br>
参考：<br>
https://docs.djangoproject.com/en/2.1/topics/forms/<br>
https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/<br>
forms.py:
```
from django import forms

class ProjectForm(forms.Form):
    name = forms.CharField(label="名称",max_length=100)
    describe = forms.CharField(label="描述",widget=forms.Textarea)
```
2、完成添加项目<br>
(1)urls.py
```
from django.urls import path
from project_app import views

urlpatterns = [
    path('project_manage/',views.project_manage),
    path('add_project/',views.add_project),
]
```
(2)views.py
```
@login_required
def add_project(request):

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            Project.objects.create(name=name,describe=describe)

            return HttpResponseRedirect('/manage/project_manage/')
    else:
        form = ProjectForm()

    return render(request,"project_manage.html",{'form':form,'type':'add'})
```
(3)project_manage.html
```
{% if type == 'add' %}
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h3 class="sub-header">添加项目</h3>
            <form action="/manage/add_project/" method="post">
                {% csrf_token %}
                {{ form.as_p }}
                <button type="submit" class="btn btn-success">提交</button>
            </form>
          </div>
        </div>
        {% endif %}
```
* {{ form.as_table }} 将它们作为表单封装在```<tr>```标签中<br>
* {{ form.as_p }} 将它们封装在```<p>```标签中<br>
* {{ form.as_ul }} 将它们封装在```<li>```标签中<br>

(4)添加编辑、删除功能
project_manage.html：
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
                  <th>操作</th>
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
                  <td>
                      <a href="/manage/edit_project/{{ project.id }}/">编辑</a>
                      <a href="/manage/delete_project/{{ project.id }}/">删除</a>
                  </td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
        {% endif %}
```

3、编辑项目<br>
(1)重构forms.py
```
from django import forms
from .models import Project

'''
class ProjectForm(forms.Form):
    name = forms.CharField(label="名称",max_length=100)
    describe = forms.CharField(label="描述",widget=forms.Textarea)
    status = forms.BooleanField(label="状态")
'''

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['create_time']


```
(1)urls.py
```
from django.urls import path
from project_app import views

urlpatterns = [
    path('project_manage/',views.project_manage),
    path('add_project/',views.add_project),
    path('edit_project/<int:pid>/',views.edit_project),
]
```
(2)views.py
```
@login_required
def edit_project(request,pid):
    """编辑项目"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            model = Project.objects.get(id=pid)
            model.name = form.cleaned_data['name']
            model.describe = form.cleaned_data['describe']
            model.status = form.cleaned_data['status']
            model.save()
            return HttpResponseRedirect('/manage/project_manage/')
    else:
        if pid:
            form = ProjectForm(instance=Project.objects.get(id=pid))
        else:
            form = ProjectForm()
    return render(request, "project_manage.html", {'form': form, 'type': 'edit'})
```
(3)project_manage.html
```
{% if type == 'edit' %}
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h3 class="sub-header">编辑项目</h3>
          <div class="table-responsive">
            <form role="form" method="post">
                {% csrf_token %}
                {{ form.as_p }}
                <button type="submit" class="btn btn-default"
                    onclick="window.location.href='/manage/project_manage/'"
                    style="margin-right: 10px;">取消</button>
                <button type="submit" class="btn btn-success">保存</button>
            </form>
          </div>
        </div>
        {% endif %}
```

4、删除项目
(1)urls.py
```
from django.urls import path
from project_app import views

urlpatterns = [
    path('project_manage/',views.project_manage),
    path('add_project/',views.add_project),
    path('edit_project/<int:pid>/',views.edit_project),
    path('delete_project/<int:pid>/',views.delete_project),
]
```

(2)views.py
```
@login_required
def delete_project(request,pid):
    """删除项目"""
    Project.objects.get(id=pid).delete()
    return HttpResponseRedirect('/manage/project_manage/')
```
