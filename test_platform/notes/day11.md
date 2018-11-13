###接口调试页面
####一、添加接口页面
1、urls.py
```
path('debug/',views.debug),
```

2、views.py
```
#创建/调试接口
def debug(request):
    if request.method == 'GET':
        form = TestCaseForm()
        return render(request,"api_debug.html",{'form':form,"type":"debug"})
    else:
        return HttpResponse("404")
```

3、api_debug.html
```
{% extends "case_manage.html" %}
{% block api_debug %}

    <fieldset>
        <div id="legend" class="">
            <legend class="">在线postman</legend>
        </div>

        <div style="width:80%; margin-left: 20px;">
        <form action="/debug/" method="get" class="bs-example bs-example-form" role="form" style="margin-top: 30px">

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

        </form>

        </div>

        <div style="width:80%; margin-left: 20px;">
            <p>返回结果：</p>
            <textarea id="result" class="form-control" rows="10" name=textarea></textarea>
        </div>

    </fieldset>

{% endblock %}
```

####二、调试接口
1、urls.py
```
path('api_debug/',views.api_debug),
```

2、views.py
```
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
        return render(request,"api_debug.html",{"type":"debug"})
```
3、api_debug.html
```
{% extends "case_manage.html" %}
{% block api_debug %}

    <fieldset>
        <div id="legend" class="">
            <legend class="">在线postman</legend>
        </div>

        <div style="width:80%; margin-left: 20px;">
        <form action="/debug/" method="get" class="bs-example bs-example-form" role="form" style="margin-top: 30px">

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

        $(document).ready(function(){
            $("#send").click(function(){
                <!--jQuery val()方法:www.runoob.com/jquery/html-val.html-->
                let url = $("#req_url").val();
                let method = $('input[name="req_method"]:checked').val();
                let parameter = $("#req_parameter").val();
                let req_type = $('input[name="req_type"]:checked').val();
                let header = $("#req_header").val();

                //console.log(url,method)
                //window.alert("hello jq");
                if(url === ""){
                    window.alert("url不能为空");
                }else if(method === ""){
                    window.alert("方法为必选项");
                }else if(parameter === ""){
                    parameter = "{}";
                }

                <!--jQuery ajax - post()方法:www.w3school.com.cn/jquery/ajax_post.asp-->
                //向后端发送post请求
                 $.post("/interface/api_debug/",{
                     "req_url":url,
                     "req_method":method,
                     "req_parameter":parameter
                 },function(result){
                    $("#result").html(result);
                  });
            });

        });
    </script>
    
{% endblock %}
```
