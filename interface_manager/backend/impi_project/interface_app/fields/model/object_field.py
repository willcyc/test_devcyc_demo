#coding:utf-8
import json
from django.db import models

class ObjectField(models.TextField):
    """字典类型的表"""
    description = "Stores a python dict"

    def __init__(self,*args,**kwargs):
        super(models.TextField,self).__init__(*args,**kwargs)

    def from_db_value(self,value,expression,connection,context):
        """从数据库读取，只处理两种情况，none和不是none"""
        if value is None:
            return value
        try:
            ret = json.loads(value)
        except:
            return None
        else:
            return ret

    def to_python(self, value):
        """to_python()通过反序列化和从表单使用的clean()方法调用。
            作为一般规则，to_python()应优雅的处理以下任何参数：
            正确类型的实例
            字符串
            None（如果字段允许null=True）
        """
        if value is None:
            value = dict()

        if isinstance(value,dict):
            return value

        try:
            ret = json.loads(value)
        except:
            return None
        else:
            return ret

    def get_prep_value(self,value):
        """保存数据的时候调用"""
        if value is None:
            return value
        return json.dumps(value,ensure_ascii=False)