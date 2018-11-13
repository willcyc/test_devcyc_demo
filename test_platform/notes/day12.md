###保存用例
1、保存用例
（1）urls.py
```
path('save_case/',views.save_case),
```

（2）api_debug.html
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

（3）views.py
```
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
```
