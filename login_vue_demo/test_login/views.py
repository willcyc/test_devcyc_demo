import json
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render

# Create your views here.

users = [
    {"name":"test1","pwd":"test1"},
    {"name":"test2","pwd":"test2"},
]

def demo1(request):
    return render(request,'demo1.html')

def demo2(request):
    return render(request,'demo2.html')

def demo3(request):
    return render(request,'demo3.html')

def demo4(request):
    return render(request,'demo4.html')

def demo5(request):
    return render(request,'demo5_chuandishuju.html')

def demo6(request):
    return render(request,'demo6_fuzujianchuandishuju.html')

def demo7(request):
    return render(request,'demo7_zizujianchuandishuju.html')

def demo8(request):
    return render(request,'demo8.html')

def demo9(request):
    return render(request,'demo9.html')

def demo10(request):
    return render(request,'demo10.html')

def login_action(request):
    if "POST" == request.method:
        body = request.body
        res = json.loads(body)
        if "name" not in res and "pwd" not in res:
            return JsonResponse({"success":False},safe=False)
        name = res["name"]
        pwd = res["pwd"]

        for u in users:
            if u["name"] == name and u["pwd"] == pwd:
                return JsonResponse({"success":True},safe=False)
            else:
                return JsonResponse({"success":False},safe=False)
    else:
        return HttpResponse(status=404)