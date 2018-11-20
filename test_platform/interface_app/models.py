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