from django.db import models
from project_app.models import Module
# Create your models here.
class TestCase(models.Model):
    """测试用例表 """
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    name = models.CharField("名称",max_length=100,blank=False,default="")
    #https://www.cnblogs.com/ccorz/p/Django-models-zhong-guan-yublank-yunull-de-bu-chon.html
    url = models.TextField("URL",default="")
    req_method = models.CharField("方法", max_length=10,default="")
    req_type = models.CharField("参数类型", max_length=10, default="")
    req_header = models.TextField("header",  default="")
    req_parameter = models.TextField("参数", default="")
    resp_assert = models.TextField("验证", default="")
    create_time = models.DateTimeField("创建时间", auto_now=True)

    def __str__(self):
        return self.name

class TestTask(models.Model):
    """测试任务表 """
    name = models.CharField("名称",max_length=100,blank=False,default="")
    describe = models.TextField("描述", default="")
    status = models.IntegerField("状态", default=0)   #未执行、执行中、排队中、执行结束...
    cases = models.TextField("关联用例", default="")
    create_time = models.DateTimeField("创建时间", auto_now=True)

    def __str__(self):
        return self.name

class TestResult(models.Model):
    """测试结果表 """
    name = models.CharField("名称",max_length=100,blank=False,default="")
    task = models.ForeignKey(TestTask,on_delete=models.CASCADE)
    error = models.IntegerField("错误用例")
    failure = models.IntegerField("失败用例")
    skipped = models.IntegerField("跳过用例")
    tests = models.IntegerField("用例总数")
    run_time = models.FloatField("运行时长")
    result = models.TextField("详细",default="")
    create_time = models.DateTimeField("创建时间", auto_now=True)

    def __str__(self):
        return self.name