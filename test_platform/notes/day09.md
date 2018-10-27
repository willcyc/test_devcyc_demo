####参考：
https://docs.djangoproject.com/zh-hans/2.1/topics/testing/overview/<br>
https://docs.djangoproject.com/en/2.1/topics/testing/tools/<br>

1、django模型（models.py）测试：<br>
测试模型（models.py）的增、删、改、查
```
from django.test import TestCase
from django.contrib.auth.models import User

#django-models测试用例
class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("test001","test001@mail.com","test123456")

    def test_user_create(self):
        """测试创建用户"""
        User.objects.create_user("test002", "test002@mail.com", "test123456")
        user = User.objects.get(username="test002")
        #print(user.email)
        #print(user.password)
        self.assertEqual(user.email, 'test002@mail.com')

    def test_user_select(self):
        """测试查询用户数据"""
        user = User.objects.get(username="test001")
        #print(user.email)
        #print(user.password)
        self.assertEqual(user.email, 'test001@mail.com')

    def test_user_update(self):
        """测试更新用户数据"""
        user = User.objects.get(username="test001")
        user.username = "test003"
        user.email = "test003@email.com"
        user.save()
        user2 = User.objects.get(username="test003")
        self.assertEqual(user2.email, 'test003@email.com')

    def test_user_delete(self):
        """测试删除用户数据"""
        user = User.objects.get(username="test001")
        user.delete()
        user2 = User.objects.all()
        #print(user2)
        #print(len(user2))
        self.assertEqual(len(user2),0)
```
运行测试用例：
```
python manage.py test user_app.tests.tests.UserTestCase
```
###注：测试数据不会写在真实数据库中，测试用例之间也不会互相影响

2、django单元/接口（views.py）测试
```
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

#django-views测试用例
class IndexTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index(self):
        """测试index.html页面"""
        response = self.client.get('/')
        print(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

class LoginActionTest(TestCase):

    def setUp(self):
        User.objects.create_user("test001", "test001@mail.com", "test123456")
        self.client = Client()

    def test_login_null(self):
        """测试用户名、密码为空"""
        login_data = {"username":"","password":""}
        response = self.client.post('/login_action/',data=login_data)
        login_html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("用户名或密码不能为空",login_html)

    def test_login_error(self):
        """测试用户名、密码错误"""
        login_data = {"username":"error","password":"error"}
        response = self.client.post('/login_action/',data=login_data)
        login_html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("用户名或密码错误",login_html)

    def test_login_success(self):
        """登录成功"""
        login_data = {"username":"test001","password":"test123456"}
        response = self.client.post('/login_action/',data=login_data)
        login_html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 302)
```
运行测试用例：
```
python manage.py test user_app.tests.tests
```
对于views.py的测试：
* django提供 Client() 来模拟发送HTTP请求;
* 从形式上看，更像是接口测试，但它又全面验证了viesw.py中的代码逻辑。所以，也可以认为是单元测试;
* views.py 是离不开 models.py 的，比如要获取项目管理列表，所以，多数时候还需要初始化创建测试数据;

3、运行测试粒度
```
# Run all the test in porject
$ ./manage.py test

# Run all the tests found within the 'animals' package
$ ./manage.py test user_app.tests

# Run all the tests in the animals.tests module
$ ./manage.py test user_app.tests.tests

# Run just one test case
$ ./manage.py test user_app.tests.tests.UserTestCase

# Run just one test method
$ ./manage.py test user_app.tests.tests.UserTestCase.test_user_select
```

4、django UI（templates/）测试
```
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver import Firefox
from time import sleep
from django.contrib.auth.models import User
from project_app.models import Project

class LoginTests(StaticLiveServerTestCase):
    #fixtures = ['user-data.json']

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.driver = Firefox()
        self.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        super().tearDownClass()

    def setUp(self):
        """初始化数据"""
        User.objects.create_user("test01", "test01@mail.com", "test123456")
        Project.objects.create(name="测试平台测试数据", describe="描述")

    def test_login_null(self):
        """用户名、密码为空"""
        self.driver.get('%s%s' % (self.live_server_url, '/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('')
        sleep(1)
        self.driver.find_element_by_id("LoginButton").click()
        sleep(2)
        error_hint = self.driver.find_element_by_id("error").text
        #print(error_hint)
        self.assertEqual("用户名或密码不能为空",error_hint)

```