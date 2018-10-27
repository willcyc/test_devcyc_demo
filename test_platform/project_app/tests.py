from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from project_app.models import Project

# Create your tests here.
class ProjectTest(TestCase):
    """项目管理"""
    def setUp(self):
        User.objects.create_user("test001", "test001@mail.com", "test123456")
        Project.objects.create(name="测试平台测试数据",describe="描述")
        self.client = Client()
        login_data = {"username": "test001", "password": "test123456"}
        response = self.client.post('/login_action/', data=login_data)

    def test_project_manage(self):
        """查询数据"""
        response = self.client.get('/manage/project_manage/')
        project_html = response.content.decode("utf-8")
        print(project_html)
        self.assertEqual(response.status_code, 200)
        self.assertIn("退出",project_html)
        self.assertIn("测试平台测试数据",project_html)

    def test_create_project_manage(self):
        """创建数据"""
        Project.objects.create(name="测试平台测试数据001", describe="描述001")
        response = self.client.get('/manage/project_manage/')
        project_html = response.content.decode("utf-8")
        print(project_html)
        self.assertEqual(response.status_code, 200)
        self.assertIn("退出",project_html)
        self.assertIn("测试平台测试数据001",project_html)
        self.assertIn("描述001", project_html)

    def test_update_project_manage(self):
        """修改数据"""
        project = Project.objects.get(name="测试平台测试数据")
        project.name = "测试平台测试数据013"
        project.describe = "描述013"
        project.save()
        response = self.client.get('/manage/project_manage/')
        project_html = response.content.decode("utf-8")
        print(project_html)
        self.assertEqual(response.status_code, 200)
        self.assertIn("退出",project_html)
        self.assertIn("测试平台测试数据013",project_html)
        self.assertIn("描述013", project_html)

    def test_delete_project_manage(self):
        """删除数据"""
        project = Project.objects.get(name="测试平台测试数据")
        project.delete()
        project2 = Project.objects.all()
        self.assertEqual(len(project2), 0)
