import requests
import json
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from interface_app.forms import TestCaseForm
from interface_app.models import TestCase
from project_app.models import Module,Project
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
#获取项目模块列表
def get_porject_list(request):
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
    return JsonResponse({"success":"true","data":dataList})


#用例列表
def case_manage(request):
    testcases = TestCase.objects.all().order_by("id")

    paginator = Paginator(testcases, 3)  #每页3条数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)  # 如果页数不是整型, 取第一页
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)  #如果页数超出查询范围，取最后一页

    if request.method == 'GET':
        return render(request,"case_manage.html",{"type":"list","testcases":contacts})
    else:
        return HttpResponse("404")

#用例搜索
def search_case_name(request):
    if request.method == 'GET':
        case_name = request.GET.get('case_name','')
        case_method = request.GET.get('case_method','')

        cases = TestCase.objects.filter(name__contains=case_name).order_by("id")

        paginator = Paginator(cases, 3)  # 每页3条数据
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)  # 如果页数不是整型, 取第一页
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)  # 如果页数超出查询范围，取最后一页

        return render(request, "case_manage.html", {"type": "list",
                                                    "testcases": contacts,
                                                    "case_name": case_name,
                                                    "case_method":case_method
                                                    })

    else:
        return HttpResponse("404")

#创建/调试用例
def add_case(request):
    if request.method == 'GET':
        form = TestCaseForm()
        return render(request,"add_case.html",{'form':form,"type":"add"})
    else:
        return HttpResponse("404")
        
#调试接口
def api_debug(request):
    if request.method == "POST":
        url = request.POST.get("req_url")
        method = request.POST.get("req_method")
        parameter = request.POST.get("req_parameter")
        header = request.POST.get("header")
        headers = json.loads(header.replace("'","\""))
        payload = json.loads(parameter.replace("'", "\"")) #loads()：将字符串转换为字典;replace()：将单引号替换为双引号

        if method == "get":
            r = requests.get(url,headers = headers,params=payload)
        elif method == "post":
            r = requests.post(url,headers = headers,data=payload)

        return HttpResponse(r.text)
    else:
        return render(request,"add_case.html",{"type":"debug"})

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

        if name == "" or url == "" or method == "" or req_type == "" or module_name == "":
            return HttpResponse("参数不能为空！")
        elif parameter == "":
            parameter = "{}"
        elif header == "":
            header = "{}"

        module_obj = Module.objects.get(name=module_name)
        case = TestCase.objects.create(module=module_obj,name=name,url=url,
                                       req_method=method,req_type=req_type,
                                       req_header=header,req_parameter=parameter
                                       )
        if case is not None:
            return HttpResponse("保存成功！")

    else:
        return HttpResponse("404")

#编辑/调试用例
def debug_case(request,cid):
    #print("调试用例id:",cid)
    if request.method == 'GET':
        form = TestCaseForm()
        return render(request,"debug_case.html",{'form':form,"type":"debug"})
    else:
        return HttpResponse("404")

#获取接口信息
def get_case_info(request):
    if request.method == "POST":
        case_id = request.POST.get("caseId","")
        #print(case_id)
        case_obj = TestCase.objects.get(pk=case_id)

        mid = case_obj.module_id    #获取模块id
        #print("模块id:",mid)
        module_obj = Module.objects.get(id=mid)
        module_name = module_obj.name   #获取模块名称

        pid = module_obj.project_id   #获取项目id
        #print("项目id：",pid)
        project_obj = Project.objects.get(id=pid)
        project_name = project_obj.name   #获取项目名称

        if case_id == "":
            return JsonResponse({"success":"false","message":"case id Null"})
        else:
            case_info = {
                "project_name":project_name,
                "module_name":module_name,
                "name":case_obj.name,
                "url":case_obj.url,
                "req_method":case_obj.req_method,
                "req_type":case_obj.req_type,
                "req_header":case_obj.req_header,
                "req_parameter":case_obj.req_parameter,
            }
            return JsonResponse({"success": "true", "message": "ok","data":case_info})
    else:
        return HttpResponse("404")

#验证预期结果
def api_assert(request):
    if request.method == 'POST':
        result_text = request.POST.get("result","")
        assert_text = request.POST.get("assert","")

        if result_text == "" or assert_text == "":
            return JsonResponse({"success":"false","message":"验证数据不能为空！"})
        try:
            assert assert_text in result_text
        except AssertionError:
            return JsonResponse({"success": "false", "message": "验证失败！"})
        else:
            return JsonResponse({"success": "true", "message": "验证成功！"})
    else:
        return HttpResponse("404")