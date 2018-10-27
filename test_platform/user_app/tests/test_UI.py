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

    def test_login_error(self):
        """用户名、密码错误"""
        self.driver.get('%s%s' % (self.live_server_url, '/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('lslsls')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('123456')
        sleep(1)
        self.driver.find_element_by_id("LoginButton").click()
        sleep(2)
        error_hint = self.driver.find_element_by_id("error").text
        #print(error_hint)
        self.assertEqual("用户名或密码错误！",error_hint)

    def test_login_success(self):
        """用户名、密码正确"""
        self.driver.get('%s%s' % (self.live_server_url, '/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('test01')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('test123456')
        sleep(1)
        self.driver.find_element_by_id("LoginButton").click()
        sleep(2)
        login_text = self.driver.find_element_by_class_name("navbar-brand").text
        self.assertEqual("测试平台",login_text)

class ProjectManageTest(StaticLiveServerTestCase):
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
        """登录"""
        User.objects.create_user("test01", "test01@mail.com", "test123456")
        Project.objects.create(name="测试平台测试数据", describe="描述")
        self.driver.get('%s%s' % (self.live_server_url, '/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('test01')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('test123456')
        sleep(1)
        self.driver.find_element_by_id("LoginButton").click()

    def test_select_project(self):
        """查询"""
        name = self.driver.find_element_by_id("list").text
        #print(name)
        self.assertIn("测试平台测试数据",name)


    def test_create_project(self):
        """创建项目"""
        self.driver.find_element_by_id("CreateButton").click()
        sleep(2)
        name_input = self.driver.find_element_by_name("name")
        name_input.send_keys("测试平台项目001")
        describe_input = self.driver.find_element_by_name("describe")
        describe_input.send_keys("这是测试平台项目001的表单")
        sleep(2)
        self.driver.find_element_by_id("Create").click()
        sleep(2)
        name = self.driver.find_element_by_id("list").text
        self.assertIn("这是测试平台项目001的表单", name)

    def test_update_project(self):
        """修改项目"""
        self.driver.find_element_by_id("update").click()
        sleep(2)
        name_input = self.driver.find_element_by_name("name")
        name_input.clear()
        name_input.send_keys("测试平台项目002")
        self.driver.find_element_by_id("save").click()
        sleep(2)
        name = self.driver.find_element_by_id("list").text
        self.assertIn("测试平台项目002", name)

    def test_delete_project(self):
        """删除项目"""
        self.driver.find_element_by_id("delete").click()
        sleep(2)
        name = self.driver.find_element_by_id("list").text
        # print(name)
        self.assertNotIn("测试平台测试数据", name)



