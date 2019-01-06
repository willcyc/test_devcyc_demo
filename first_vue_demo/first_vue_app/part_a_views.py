from django.shortcuts import render
from django.http import JsonResponse

def part_a(request):
    return render(request,'part_a.html')

def part_b(request):
    return render(request,'part_b.html')

def part_c(request):
    return render(request,'part_c.html')

def part_d(request):
    return render(request,'part_d.html')

def part_e(request):
    return render(request,'part_e.html')

def get_array(request):
    ret = ["apple","orange","banana"]
    return JsonResponse(ret,safe=False)

def get_json(request):
    ret = {
        "apple":10,
        "orange":5,
        "banana":3
    }
    return JsonResponse(ret,safe=False)