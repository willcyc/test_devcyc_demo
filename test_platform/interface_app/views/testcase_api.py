import json
import requests
from test_platform import common
from interface_app.models import TestCase
from project_app.models import Project, Module


#获取项目模块列表
def get_porject_list(request):
    if request.method == "GET":
        project_list = Project.objects.all()
        dataList = []
        for project in project_list:
            project_dict = {
                "name":project.name
            }

            module_list = Module.objects.filter(project_id=project.id)
            if len(module_list) != 0:
                module_name = []
                for module in module_list:
                    module_name.append(module.name)

                project_dict["moduleList"] = module_name
                dataList.append(project_dict)
        #return JsonResponse({"success":"true","data":dataList})
        return common.response_succeed(data=dataList)
    else:
        return common.response_failed("请求方法错误！")  #return: 项目接口列表

#调试接口
def api_debug(request):
    if request.method == "POST":
        url = request.POST.get("req_url","")
        method = request.POST.get("req_method","")
        type = request.POST.get("req_type","")
        parameter = request.POST.get("req_parameter","")
        header = request.POST.get("req_header","")

        if url == "" or method == "" or type == "":
            return common.response_failed("必传参数不能为空！")

        payload = json.loads(parameter.replace("'", "\""))  # loads()：将字符串转换为字典;replace()：将单引号替换为双引号
        if method == "get":
            if type == "from":
                r = requests.get(url,params=payload)
            else:
                return common.response_failed("参数类型错误!")

        elif method == "post":
            if type == "from":
                r = requests.post(url, data=payload)
            elif type == "json":
                r = requests.post(url, json=payload)
            else:
                return common.response_failed("参数类型错误!")

        return common.response_succeed(data=r.text)

    else:
        return common.response_failed("请求方法错误")

#验证预期结果
def api_assert(request):
    if request.method == 'POST':
        result_text = request.POST.get("result","")
        assert_text = request.POST.get("assert","")

        if result_text == "" or assert_text == "":
            return common.response_failed("验证的数据不能为空！")
        try:
            assert assert_text in result_text
        except AssertionError:
            return common.response_failed("验证失败!")
        else:
            return common.response_succeed("验证成功!")
    else:
        return common.response_failed("请求方法错误")

#保存用例
def save_case(request):
    if request.method == "POST":
        name = request.POST.get("name","")
        url = request.POST.get("req_url","")
        method = request.POST.get("req_method","")
        parameter = request.POST.get("req_parameter","")
        req_type = request.POST.get("req_type","")
        header = request.POST.get("header","")
        module_name = request.POST.get("module","")
        assert_text = request.POST.get("assert_text","")

        if name == "" or url == "" or method == "" or req_type == "" or module_name == "" or assert_text == "":
            return common.response_failed("必传参数不能为空！")
        elif parameter == "":
            parameter = "{}"
        elif header == "":
            header = "{}"

        module_obj = Module.objects.get(name=module_name)
        case = TestCase.objects.create(module=module_obj,name=name,url=url,
                                       req_method=method,req_type=req_type,
                                       req_header=header,req_parameter=parameter,resp_assert=assert_text
                                       )
        if case is not None:
            return common.response_succeed("保存成功！")

    else:
        return common.response_failed("请求方法错误！")

#获取接口信息
def get_case_info(request):
    if request.method == "POST":
        case_id = request.POST.get("caseId","")
        #print(case_id)
        if case_id == "":
            return common.response_failed("用例id为空")

        case_obj = TestCase.objects.get(pk=case_id)

        mid = case_obj.module_id    #获取模块id
        #print("模块id:",mid)
        module_obj = Module.objects.get(id=mid)
        module_name = module_obj.name   #获取模块名称

        pid = module_obj.project_id   #获取项目id
        #print("项目id：",pid)
        project_obj = Project.objects.get(id=pid)
        project_name = project_obj.name   #获取项目名称

        case_info = {
            "projectName":project_name,
            "moduleName":module_name,
            "name":case_obj.name,
            "url":case_obj.url,
            "reqMethod":case_obj.req_method,
            "reqType":case_obj.req_type,
            "reqHeader":case_obj.req_header,
            "reqParameter":case_obj.req_parameter,
            "assertText":case_obj.resp_assert,
        }
        return common.response_succeed(data=case_info)
    else:
        return common.response_failed("请求方法错误！")
