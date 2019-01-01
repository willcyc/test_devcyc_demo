from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def demo(request):
    return render(request,'vue_demo.html')

def demo2(request):
    return render(request,'vue_demo2.html')