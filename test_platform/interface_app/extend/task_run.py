#运行某任务下的用例cases --单元测试框架 + 数据驱动
import sys
import unittest
import json
from ddt import ddt,data,unpack,file_data
import requests
import xmlrunner
from os.path import dirname,abspath

BASE_DIR = dirname(dirname(dirname(abspath(__file__))))  #abspath(__file__)：当前文件的绝对路径；dirname上一级文件
BASE_PATH = BASE_DIR.replace("\\","/")
#sys.path.append(BASE_PATH)  #将获取到的项目根目录添加到环境变量中
TASK_PATH = BASE_PATH + "/resource/tasks/"  #任务的目录
#print("运行测试文件：",BASE_PATH)

@ddt
class MyTest(unittest.TestCase):

	@unpack
	@file_data(TASK_PATH + "cases_data.json")

	def test_demo(self, url, method, type_,header,parameter,assert_):
		#print("URL:",url)
		#print("方法:",method)
		#print("参数：",parameter)

		if header == "{}":
			header_dict = {}
		else:
			header_dict = json.loads(header.replace("\'","\""))  #将json字符串转化为字典、将单引号转化为双引号

		if parameter == "{}":
			parameter_dict = {}
		else:
			parameter_dict = json.loads(parameter.replace("\'","\""))  #将json字符串转化为字典、将单引号转化为双引号

		if method == "get":
			if type_ == "from":
				r = requests.get(url, headers=header_dict, params=parameter_dict)
				self.assertIn(assert_, r.text)

		elif method == "post":
			if type_ == "from":
				r = requests.post(url, headers=header_dict, data=parameter_dict)
				self.assertIn(assert_, r.text)
			elif type_ == "json":
				r = requests.post(url, headers=header_dict, json=parameter_dict)
				self.assertIn(assert_, r.text)

#运行测试用例
def run_cases():
    with open(TASK_PATH + 'results.xml', 'wb') as output:  # 指定report存放位置为当前目录
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)


if __name__ == '__main__':
    run_cases()