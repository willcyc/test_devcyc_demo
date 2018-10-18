from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project_app.models import Project
from project_app.forms import ProjectForm
from django.http import HttpResponseRedirect

# Create your views here.
@login_required
def project_manage(request):
    """项目列表管理"""
    #username = request.COOKIES.get('user','')  #读取浏览器cookie
    username = request.session.get('user','')   #读取浏览器session
    project_all = Project.objects.all()
    return render(request, "project_manage.html",{"user":username,"projects":project_all,"type":"list"})

'''
@login_required
def add_project(request):
    """添加项目"""
    return render(request, "project_manage.html",{"type":"add"})
'''

@login_required
def add_project(request):

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            Project.objects.create(name=name,describe=describe)

            return HttpResponseRedirect('/manage/project_manage/')
    else:
        form = ProjectForm()

    return render(request,"project_manage.html",{'form':form,'type':'add'})

@login_required
def edit_project(request,pid):

    project = Project.objects.get(id=pid)
    name = project.name
    describe = project.describe

    if request.method == 'POST':
        form = ProjectForm(instance=project,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/manage/project_manage/')
    else:
        form = ProjectForm()

    #context = {'project':project,'name':name,'describe':describe,'form':form}
    return render(request, "project_manage.html", {'form': form, 'type': 'edit','project':project})