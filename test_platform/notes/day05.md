
### Django 创建表：

1、在models.py创建数据库表：
```python
from django.db import models


class Project(models.Model):
    """
    项目表
    """
    name = models.CharField("名称", max_length=100, blank=False, default="")
    describe = models.TextField("描述", default="")
    status = models.BooleanField("状态：", default=True)
    create_time = models.DateTimeField("创建时间", auto_now=True)

    def __str__(self):
        return self.name


class Module(models.Model):
    """
    模块表
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=100, blank=False, default="")
    describe = models.TextField("描述", default="")
    create_time = models.DateTimeField("创建时间", auto_now=True)

    def __str__(self):
        return self.name
```
2、把在 models.py 中创建的表映射到admin后台进行管理<br>
在admin.py中：
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

3、创建表单：
```
python manage.py makemigrations
python manage.py migrate
```

数据类型查看 ```C:\python3.5\Lib\site-packages\django\db\models\fields\__init__.py```


### 数据库表操作：
* 进入方式
```
python manage.py shell
```

* 创建
```python
Project.objects.create()
```

* 查询
```python
Project.objects.all()
Project.objects.get(pk=1)
Project.objects.filter(status=1)
Project.objects.filter(name__contains='项目')
```

* 更新
```python
g = Project.objects.get(name='xxx测试项目')
g.status=0
g.save()

Project.objects.select_for_update().filter(name__contains='项目').update(describe='')
```

* 删除
```python
Project.objects.get(name='xxx测试项目').delete()
```

4、在view.py视图中读取数据库中内容：
```
@login_required
def project_manage(request):
    """项目列表管理"""
    #username = request.COOKIES.get('user','')  #读取浏览器cookie
    username = request.session.get('user','')   #读取浏览器session
    project_all = Project.objects.all()
    return render(request, "project_manage.html",{"user":username,"projects":project_all})
```

5、在project_manage.html中显示数据库中内容：
```
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
```