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
        print("parameter123:",parameter)
        print("header123:",header)
        if url == "" or method == "" or type == "":
            return common.response_failed("必传参数不能为空！")

        try:
            headers = json.loads(header.replace("'", "\""))
            payload = json.loads(parameter.replace("'", "\""))  # loads()：将字符串转换为字典;replace()：将单引号替换为双引号
            print("payload123:",payload)
            print("headers123:",headers)
        except json.decoder.JSONDecodeError:
            return common.response_failed("格式解析错误，请检查header或参数的格式是否正确!")

        if method == "get":
            if type == "from":
                r = requests.get(url,headers=headers,params=payload)
            else:
                return common.response_failed("参数类型错误!")

        elif method == "post":
            if type == "from":
                r = requests.post(url, headers=headers,data=payload)
            elif type == "json":
                r = requests.post(url,headers=headers,json=payload)
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
            assertList = assert_text.split()
            #print("assertList:", assertList)
            for asserttext in assertList:
                assert asserttext in result_text
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

        if name == "" or url == "" or method == "" or req_type == "" or module_name == "":
            return common.response_failed("必传参数不能为空！")
        elif parameter == "":
            parameter = "{}"
        elif header == "":
            header = "{}"
        elif assert_text == "":
            return common.response_failed("保存前，请先进行验证操作！")

        module_obj = Module.objects.get(name=module_name)
        case = TestCase.objects.create(
                                    module=module_obj,
                                    name=name,
                                    url=url,
                                    req_method=method,
                                    req_type=req_type,
                                    req_header=header,
                                    req_parameter=parameter,
                                    resp_assert=assert_text
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

        try:
            case_obj = TestCase.objects.get(pk=case_id)
        except TestCase.DoesNotExist:
            return common.response_failed("该用例id不存在！")

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
        print(case_info)
        return common.response_succeed(data=case_info)
    else:
        return common.response_failed("请求方法错误！")

#更新用例接口
def update_case(request):
    if request.method == "POST":
        case_id = request.POST.get("cid","")
        name = request.POST.get("name","")
        url = request.POST.get("req_url","")
        method = request.POST.get("req_method","")
        parameter = request.POST.get("req_parameter","")
        req_type = request.POST.get("req_type","")
        header = request.POST.get("header","")
        module_name = request.POST.get("module","")
        assert_text = request.POST.get("assert_text","")
        print("接口ID：",case_id)

        if name == "" or url == "" or method == "" or req_type == "" or module_name == "":
            return common.response_failed("必传参数不能为空！")
        elif parameter == "":
            parameter = "{}"
        elif header == "":
            header = "{}"
        elif assert_text == "":
            return common.response_failed("保存前，请先进行验证操作！")

        module_obj = Module.objects.get(name=module_name)
        case_obj = TestCase.objects.filter(id=case_id).update(
                module=module_obj,
                name=name,
                url=url,
                req_method=method, 
                req_header=header,
                req_type=req_type,
                req_parameter=parameter,
                resp_assert=assert_text
            )
        print("case_obj：",case_obj)
        if case_obj == 1:
            return common.response_succeed("更新成功！")
        else:
            return common.response_failed("更新失败！")

    else:
        return common.response_failed("请求方法错误！")

#获取测试用例列表
def get_case_list(request):
    if request.method == "GET":
        #项目 -> 模块 -> 用例
        cases_list = []

        projects = Project.objects.all()
        for project in projects:
            modules = Module.objects.filter(project_id=project.id)
            for module in modules:
                cases = TestCase.objects.filter(module_id=module.id)
                for case in cases:
                    case_info = project.name + "->" + module.name + "->" +case.name
                    cases_dict = {
                        "id":case.id,
                        "name":case_info
                    }
                    cases_list.append(cases_dict)

        return common.response_succeed(data=cases_list)

    else:
        return common.response_failed("请求方法错误")