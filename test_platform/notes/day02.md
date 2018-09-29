1、环境搭建：<br>
python3.7+Django2.1.1<br>

2、创建项目：<br>
(1)django-admin<br>
(2)django-admin startproject test_paltform（项目名）<br>

3、django项目目录<br>
（1）manage.py： Django 项目的命令行工具；<br>
（2）__init__.py：空文件，表示当前目录是一个Python 包；<br>
（3）settings.py：Django 项目的配置文件；<br>
（4）urls.py：Django 项目的 URL 声明；<br>
（5）wsgi.py：项目运行在 WSGI 兼容的Web服务器上的入口；<br>

4、运行Django服务命令：
```
python manage.py runserver
python manage.py runserver 0.0.0.0:8000
```

5、创建应用
```
python manage.py startapp user_app
```

6、在settings.py中的INSTALLED_APPS中添加创建的应用：
```
INSTALLED_APPS = [
    'user_app.apps.UserAppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
- django.contrib.admin -- 管理员站点
- django.contrib.auth -- 认证授权系统
- django.contrib.contenttypes -- 内容类型框架
- django.contrib.sessions -- 会话框架
- django.contrib.messages -- 消息框架
- django.contrib.staticfiles -- 管理静态文件的框架

7、MTV设计模式
 - M 代表模型（Model），数据存取层，该层处理与数据相关的所有事物：如何存取、包含哪些行为以及数据之间的关系等
 - T 代表模板（Template），即表现层。该层处理与表现相关的决定：如何在页面和其他类型的文档中进行显示
 - V 代表视图（View），即业务逻辑层。该层包含存取模型及调取恰当模型的相关逻辑，可看作模板与模型之间的桥梁

