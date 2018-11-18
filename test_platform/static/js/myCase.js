//获取指定case_id的用例信息
var CaseInit = function (case_id) {

    function getCaseInfo(){
        // 获取用例的信息
        $.post("/interface/get_case_info/", {
            "caseId":case_id,
        }, function (resp) {
            if(resp.success === "true"){
                let result = resp.data;
                console.log("结果",result);
                document.getElementById("req_name").value = result.name;  //用js在用例名称输入框中输入内容
                document.getElementById("req_url").value = result.url;
                document.getElementById("req_header").value = result.req_header;
                document.getElementById("req_parameter").value = result.req_parameter;
                if(result.req_method == 'post'){
                    document.getElementById("post").setAttribute("checked","");  //用js给标签添加属性
                }
                if (result.req_type == 'json'){
                    document.getElementById("json").setAttribute("checked","");
                }

                //初始化菜单
                ProjectInit('project_name','module_name',result.project_name,result.module_name);
            }else{
                window.alert("用例id不存在！");
            }
            //$("#result").html(resp);
        });
    }
    // 调用getCaseInfo函数
    getCaseInfo();

}