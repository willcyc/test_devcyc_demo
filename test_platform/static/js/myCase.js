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
                document.getElementById("req_header").value = result.reqHeader;
                document.getElementById("req_parameter").value = result.reqParameter;
                document.getElementById("assert_text").value = result.assertText;

                if(result.reqMethod  == 'post'){
                    document.getElementById("post").setAttribute("checked","");  //用js给标签添加属性
                }
                if (result.reqType  == 'json'){
                    document.getElementById("json").setAttribute("checked","");
                }

                //初始化菜单
                ProjectInit('project_name','module_name',result.projectName,result.moduleName);
            }else{
                window.alert(resp.message);
                return;
            }
            //$("#result").html(resp);
        });
    }
    // 调用getCaseInfo函数
    getCaseInfo();

}

//获取用例列表
var CaseListInit = function () {

    var options = "";
    function getCaseListInfo(){
        // 获取用例列表的信息
        $.get("/interface/get_case_list", {}, function (resp) {
            if(resp.success === "true"){
                console.log(resp.data);
                let cases = resp.data;
                for(let i=0; i<cases.length;i++){
                    let option = '<input type="checkbox" name=" ' + cases[i].name +
                        ' " value="' + cases[i].id + '"/> ' + cases[i].name + '<br>'
                    //console.log("123->",option)

                    options = options + option;
                }

                //console.log("结果：",options);

                let devCaselist = document.querySelector(".caselist");  //在add_task.html页面中找到caselist属性
                devCaselist.innerHTML = options;    //将options内容插入到caselist属性所在的标签中


            }else{
                window.alert(resp.message);
                return;
            }
            //$("#result").html(resp);
        });
    }
    // 调用getCaseListInfo函数
    getCaseListInfo();

}