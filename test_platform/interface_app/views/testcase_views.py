from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
#from interface_app.forms import TestCaseForm
from interface_app.models import TestCase
#from project_app.models import Module,Project
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


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
        #form = TestCaseForm()
        return render(request,"add_case.html",{"type":"add"})
    else:
        return HttpResponse("404")


#编辑/调试用例
def debug_case(request,cid):
    #print("调试用例id:",cid)
    if request.method == 'GET':
        #form = TestCaseForm()
        return render(request,"debug_case.html",{"type":"debug"})
    else:
        return HttpResponse("404")

#删除用例
def delete_case(request,cid):
    """删除用例"""
    print("cid:",cid)
    if cid is not None:
        TestCase.objects.get(id=cid).delete()
        return HttpResponseRedirect('/interface/case_manage/')
    else:
        return HttpResponseRedirect('/interface/case_manage/')