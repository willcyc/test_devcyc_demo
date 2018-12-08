#运行某任务下的用例cases --单元测试框架 + 数据驱动
import unittest
from ddt import ddt,data,unpack
import requests
import xmlrunner

@ddt
class MyTest(unittest.TestCase):

	@unpack
	@data({'url': 'http://httpbin.org/post', 'method': 'post', 'data':{'key':'value'}},
		{'url': 'https://api.github.com/events', 'method': 'get', 'data': {}})
	def test_dicts_extracted_into_kwargs(self, url, method, data):
		#print("URL:",url)
		#print("方法:",method)
		#print("参数：",data)

		if method == "post":
			r = requests.post(url,data=data)
			#print(r.json())
			self.assertEqual(2+1,4)

		if method == "get":
			r = requests.get(url,params=data)
			#print(r.text)
			self.assertEqual(2+2,4)

#运行测试用例
def run_cases():
    with open('D:/git/test_devcyc_demo/test_platform/interface_app/extend/results.xml', 'wb') as output:  # 指定report存放位置为当前目录
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)


if __name__ == '__main__':
    run_cases()