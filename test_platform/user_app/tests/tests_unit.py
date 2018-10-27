from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

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

#测试数据不会写在真实数据库中，测试用例之间也不会互相影响


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

class LogoutActionTest(TestCase):
    def setUp(self):
        User.objects.create_user("test001", "test001@mail.com", "test123456")
        self.client = Client()
        login_data = {"username": "test001", "password": "test123456"}
        response = self.client.post('/login_action/', data=login_data)
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        """登录后退出"""

        response = self.client.post('/logout/')
        login_html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 302)