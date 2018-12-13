import json,os
import threading
from time import sleep
from interface_app.models import TestTask,TestCase,TestResult
from interface_app.apps import TASK_PATH,RUN_TASK_FILE
from xml.dom import minidom

class TaskThread():
    """实现测试任务的多线程执行"""

    def __init__(self,task_id):
        self.tid = task_id

    def run_cases(self,tid):
        task_obj = TestTask.objects.get(id=tid)
        cases_list = task_obj.cases.split(",")
        cases_list.pop(-1)
        print(cases_list)

        task_obj.status = 1  # 修改任务执行状态为执行中
        task_obj.save()
        # print(task_obj.cases)

        all_cases_dict = {}
        for case_id in cases_list:
            case_obj = TestCase.objects.get(id=case_id)
            case_dict = {
                "url": case_obj.url,
                "method": case_obj.req_method,
                "type_": case_obj.req_type,
                "header": case_obj.req_header,
                "parameter": case_obj.req_parameter,
                "assert_": case_obj.resp_assert
            }
            all_cases_dict[case_obj.id] = case_dict

        print(all_cases_dict)

        cases_str = json.dumps(all_cases_dict)  # json格式数据转化为字符串
        cases_data_file = TASK_PATH + "cases_data.json"  # 用例文件路径
        print(cases_data_file)
        with open(cases_data_file, "w") as f:  # 将用例写入到cases_data.json用例文件中
            f.write(cases_str)

        os.system("python " + RUN_TASK_FILE)  # 运行用例

    #保存测试结果
    def save_result(self):
        # 打开xml文档
        dom = minidom.parse(TASK_PATH + 'results.xml')

        #获取文档元素对象
        root = dom.documentElement
        ts = root.getElementsByTagName('testsuite')
        print("errors：",ts[0].getAttribute("errors"))
        print("failures：",ts[0].getAttribute("failures"))
        print("tests：",ts[0].getAttribute("tests"))

    #创建线程
    def run(self):
        threads = []
        t = threading.Thread(target=self.run_cases,args=(self.tid,))
        threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        sleep(2)
        print("测试(任务)线程运行完成之后。。。")

        self.save_result()

        task_obj = TestTask.objects.get(id=self.tid)
        task_obj.status = 2  # 修改任务执行状态为执行完成
        task_obj.save()



    def new_run(self):
        threads = []
        t = threading.Thread(target=self.run)
        threads.append(t)
        for t in threads:
            t.start()