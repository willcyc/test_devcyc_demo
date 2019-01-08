import json
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

# Create your views here.
def index(request):
    return render(request,'index.html')

def demo(request):
    return render(request,'vue_demo.html')

def demo2(request):
    return render(request,'vue_demo2.html')

def demo3(request):
    return render(request,'vue_demo3.html')

def demo4(request):
    return render(request,'vue_demo4.html')

data = ["apple","orange","banana","lemon","pear"]
def search(request):
    if "POST" == request.method:
        body = json.loads(request.body)
        print("body:",body)
        if "key" not in body:
            return JsonResponse([],safe=False)
        key = body["key"]
        ret = []
        for i in data:
            if key in i:
                ret.append(i)
        return JsonResponse(ret, safe=False)

    else:
        return HttpResponse(status=404)