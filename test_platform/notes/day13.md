###一、二级联动<br>
1、jsProject.js
```
var ProjectInit = function (_cmbProject, _cmbModule) {
    var cmbProject = document.getElementById(_cmbProject);
    var cmbModule = document.getElementById(_cmbModule);
    var dataList = [];

    //创建下拉选项
    function cmbAddOption(cmb, str, obj) {
        console.log(str);
        var option = document.createElement("option"); //创建<option></option>
        cmb.options.add(option);
        option.innerHTML = str;  //将str添加在标签中：<option>str</option>
        option.value = str;      //标签的value值：<option value="str">str</option>
        option.obj = obj;

        //<option value="项目名称">项目名称</option>

    }

    //改变项目
    function changeProject() {
        cmbModule.options.length = 0;
        //cmbModule.onchange = null;
        if (cmbProject.selectedIndex == -1) {
            return;
        }
        var item = cmbProject.options[cmbProject.selectedIndex].obj;
        for (var i = 0; i < item.moduleList.length; i++) {
            cmbAddOption(cmbModule, item.moduleList[i], null);
        }
    }

    function getProjectList(){
        // 调用项目列表接口
        $.get("/interface/get_porject_list", {}, function (resp) {
            if(resp.success === "true"){
                dataList = resp.data;
                //遍历项目/模块
                for (var i = 0; i < dataList.length; i++) {
                    cmbAddOption(cmbProject, dataList[i].name, dataList[i]);
                }

                changeProject();
                cmbProject.onchange = changeProject;
            }
            //$("#result").html(resp);
        });
    }
    // 调用getProjectList函数
    getProjectList();

}
```

2、urls.py
```
path('get_porject_list/',views.get_porject_list),
```

3、views.py(项目/模块接口)
```
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
```

4、api_debug.html
```
{% extends "case_manage.html" %}
{% block api_debug %}

    <fieldset>
        <div id="legend" class="">
            <legend class="">在线postman</legend>
        </div>

        <div style="width:80%; margin-left: 20px;">
        <form action="/debug/" method="get" class="bs-example bs-example-form" role="form" style="margin-top: 30px">

            <div class="form-group" style="height: 20px;">
                <label>项目:</label>
                <select id="project_name"></select>
            </div>

            <div class="form-group">
                <label>模块:</label>
                <select id="module_name"></select>
            </div>

            <div class="input-group">
                <span class="input-group-addon">名称</span>
                <input id="req_name" type="text" class="form-control" placeholder="name">
            </div>
            <br>

            <div class="input-group">
                <span class="input-group-addon">URL</span>
                <input id="req_url" type="text" class="form-control" placeholder="url">
            </div>
            <br>
            <div>
                <label>请求方法：</label>
                <label class="radio-inline">
                    <input type="radio" name="req_method" id="get" value="get" checked> GET
                </label>
                <label class="radio-inline">
                    <input type="radio" name="req_method" id="post" value="post"> POST
                </label>
                <label class="radio-inline">
                    <input type="radio" name="req_method" id="pub" value="put"> PUT
                </label>
                <label class="radio-inline">
                    <input type="radio" name="req_method" id="delete" value="delete"> DELETE
                </label>
            </div>

            <div style="margin-top: 10px;">
                <label>参数类型：</label>
                <label class="radio-inline">
                    <input type="radio" name="req_type" id="from" value="from" checked> form-data
                </label>
                <label class="radio-inline">
                    <input type="radio" name="req_type" id="json" value="json"> JSON
                </label>
            </div>

            <br>
            <div class="input-group">
                <span class="input-group-addon">Header</span>
                <input id="req_header" type="text" class="form-control">
            </div>
            <p style="color:#8B8989">说明：以字典的方式设置参数，如：{"content-type": "application/json"}</p>
            <br>
            <div class="input-group">
                <span class="input-group-addon">参数</span>
                <input id="req_parameter" type="text" class="form-control">
            </div>
            <p style="color:#8B8989">说明：以字典的方式设置参数，如：{"id":1, "name":"名称"}</p>
            <div style="width: 100%; height: 60px;">
                <button type="button" class="btn btn-success" id="send" style="float: right;margin-right: 10px;">调试</button>
                <button type="button" class="btn btn-success" id="save" style="float: right;margin-right: 10px;">保存</button>
            </div>

        </form>

        </div>

        <div style="width:80%; margin-left: 20px;">
            <p>返回结果：</p>
            <textarea id="result" class="form-control" rows="10" name=textarea></textarea>
        </div>

    </fieldset>

    <!--添加jQuery cdn：https://www.bootcdn.cn/jquery/-->
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>
    <!--jQuery选择器:www.runoob.com/jquery/jquery-selectors.html-->
    <script type="text/javascript">

        //初始化菜单，二级联动
        ProjectInit('project_name','module_name')
        //三级联动例子：http://www.cnblogs.com/wyp-AY/p/9363178.html

        $(document).ready(function(){
            $("#send").click(function(){
                //<!--jQuery val()方法:www.runoob.com/jquery/html-val.html-->
                let name = $("#req_name").val();
                let url = $("#req_url").val();
                let method = $('input[name="req_method"]:checked').val();
                let parameter = $("#req_parameter").val();
                let req_type = $('input[name="req_type"]:checked').val();
                let header = $("#req_header").val();

                //console.log(url,method)
                //window.alert("hello jq");
                if(name ===""){
                    window.alert("用例名称不能为空");
                }else if(url === ""){
                    window.alert("url不能为空");
                }else if(method === ""){
                    window.alert("请求方法为必选项");
                }else if(parameter === ""){
                    parameter = "{}";
                }else if(req_type === ""){
                    window.alert("参数类型为必选项");
                }else if(header === ""){
                    header = "{}";
                }

                //<!--jQuery ajax - post()方法:www.w3school.com.cn/jquery/ajax_post.asp-->
                //向后端发送post请求
                 $.post("/interface/api_debug/",{
                     "req_url":url,
                     "req_method":method,
                     "header":header,
                     "req_parameter":parameter
                 },function(result){
                    $("#result").html(result);
                  });
            });

            $("#save").click(function(){
                //<!--jQuery val()方法:www.runoob.com/jquery/html-val.html-->
                let name = $("#req_name").val();
                let url = $("#req_url").val();
                let method = $('input[name="req_method"]:checked').val();
                let parameter = $("#req_parameter").val();
                let req_type = $('input[name="req_type"]:checked').val();
                let header = $("#req_header").val();
                let module_name = $('select[id="module_name"]').val();

                console.log("类型",req_type)
                console.log("头部",header)
                console.log("模块",module_name)
                //window.alert("hello jq");
                if(name === ""){
                    window.alert("名称不能为空");
                }
                else if(url === ""){
                    window.alert("url不能为空");
                }else if(method === ""){
                    window.alert("方法为必选项");
                }else if(parameter === ""){
                    parameter = "{}";
                }else if(req_type === ""){
                    window.alert("参数类型为必选项");
                }else if(header === ""){
                    header = "{}";
                }

                //<!--jQuery ajax - post()方法:www.w3school.com.cn/jquery/ajax_post.asp-->
                //向后端发送post请求
                 $.post("/interface/save_case/",{
                     "name":name,
                     "req_url":url,
                     "req_method":method,
                     "req_parameter":parameter,
                     "req_type":req_type,
                     "header":header,
                     "module":module_name
                 },function(req){
                    $("#result").html(req);
                  });
            });
        });
    </script>


{% endblock %}
```

5、base.html
```
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <meta name="description" content="">
    <meta name="author" content="">
    <!--<link rel="icon" href="../../favicon.ico">-->

    <title>测试平台</title>

    <!-- 引用CDN样式 -->
    <!--<link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">-->
    <!--<link href="https://v3.bootcss.com/examples/signin/signin.css" rel="stylesheet">-->
    <!--<link href="https://v3.bootcss.com/examples/dashboard/dashboard.css" rel="stylesheet">-->

    <!--引用本地样式-->
    {% load static %}
    <link rel="stylesheet" type="text/css" href="{% static "css/bootstrap.min.css" %}">
    <link rel="stylesheet" type="text/css" href="{% static "css/signin.css" %}">
    <link rel="stylesheet" type="text/css" href="{% static "css/dashboard.css" %}">
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>
    <script type="text/javascript" src="{% static "js/jsProject.js" %}"></script>
    <script type="text/javascript" src="{% static "js/bootstrap.min.js" %}"></script>


  </head>

  <body>
    {% block content %}{% endblock %}
  </body>

</html>
```

###二、搜索<br>
1、urls.py
```
path('search_case_name/',views.search_case_name),
```

2、views.py
```
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
                                                    "case_name": case_name
                                                    })

    else:
        return HttpResponse("404")
```

3、case_manage.html
```
{% extends "base.html" %}
{% block content %}

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed"  data-toggle="collapse" data-target="#navbar"
                  aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">测试平台</a>
        </div>

        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
            <li><a href="#">{{ user }}</a></li>
            <li><a href="/logout">退出</a></li>
          </ul>
          <form class="navbar-form navbar-right">
            <input type="text" class="form-control" placeholder="Search...">
          </form>
        </div>
      </div>
    </nav>

    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar">
            <li><a href="/manage/project_manage/">项目管理</a></li>
            <li><a href="/manage/module_manage/">模块管理</a></li>
          </ul>
          <ul class="nav nav-sidebar">
            <li class="active"><a href="#">用例管理</a></li>
            <li><a href="/interface/task_manage/">任务管理</a></li>
          </ul>
          <ul class="nav nav-sidebar">
            <li><a href="">mockserver</a></li>
            <li><a href="">测试工具</a></li>
          </ul>
        </div>

        {% if type == 'list' %}
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h3 class="sub-header">用例列表
            <button type="button" class="btn btn-default" id="CreateButton"
                    style="float: right;"
                    onclick="window.location.href='/interface/debug/'">调试</button>
          </h3>

          <div class="table-responsive">

            <!--列表搜索-->
            <form class="navbar-form" method="get" action="/interface/search_case_name/">
                    <div class="form-group">
                        <input name="case_name" type="text" placeholder="用例名称" class="form-control">
                    </div>
                    <button type="submit" class="btn btn-success">搜索</button>
            </form>

            <table class="table table-striped" id="list">
              <thead>
                <tr>
                  <th>id</th>
                  <th>名称</th>
                  <th>URL</th>
                  <th>请求方法</th>
                  <th>创建时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {% for case in testcases %}
                <tr>
                  <td>{{ case.id }}</td>
                  <td>{{ case.name }}</td>
                  <td>{{ case.url }}</td>
                  <td>{{ case.req_method }}</td>
                  <td>{{ case.create_time }}</td>
                  <td>
                      <a href="/interface_app/edit_project/{{ project.id }}/" id="update">编辑</a>
                      <a href="/manage/delete_project/{{ project.id }}/" id="delete">删除</a>
                  </td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>

          <!-- 列表分页器 -->
            <div class="pagination">
                <span class="step-links">
                    <ul class="pagination">
                        {% if testcases.has_previous %} <!--是否有上一页-->
                            <li><a href="?case_name={{ case_name }}&page={{ testcases.previous_page_number }}">&laquo;</a></li>
                        {% endif %}                                 <!--testcases.previous_page_number：上一页是第几页-->

                        <li><a href="#">{{ testcases.number }}</a></li>  <!--testcases.number：当前页是第几页-->

                        {% if testcases.has_next %} <!--是否有下一页-->
                            {% if case_name %}
                                <li><a href="?case_name={{ case_name }}&page={{ testcases.next_page_number }}">&raquo;</a></li>
                            {% else %}                               <!--testcases.previous_page_number：下一页是第几页-->
                                <li><a href="?page={{ testcases.next_page_number }}">&raquo;</a></li>
                            {% endif %}
                        {% endif %}
                        <li><a href="#">共：{{ testcases.paginator.num_pages }} 页</a></li>
                    </ul>
                </span>
            </div>

        </div>
        {% endif %}

        {% if type == 'debug' %}
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <!--<h3 class="sub-header">在线postman接口</h3>-->

          <div class="row">
                {% block api_debug %}{% endblock %}
          </div>
        </div>
        {% endif %}

        {% if type == 'edit' %}
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h3 class="sub-header">编辑项目
            <button class="btn btn-default"
                            onclick="window.location.href='/manage/project_manage/'"
                            style="margin-left: 180px;">取消
            </button>
          </h3>
          <div class="table-responsive">
            <form role="form" method="post">
                {% csrf_token %}
                {{ form.as_p }}
                <button type="submit" id="save" class="btn btn-success">保存</button>
            </form>
          </div>
        </div>
        {% endif %}

      </div>
    </div>

{% endblock %}
```