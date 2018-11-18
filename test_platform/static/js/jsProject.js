var ProjectInit = function (_cmbProject, _cmbModule,defaultProject,defaultModule) {
    var cmbProject = document.getElementById(_cmbProject);
    var cmbModule = document.getElementById(_cmbModule);
    var dataList = [];

    //window.alert(defaultProject);
    //window.alert(defaultModule);
    //点击调试按钮，在调试用例页面中显示的项目、模块
    function cmbSelect(cmb,str) {
        for(var i=0;i<cmb.options.length;i++){
            if(cmb.options[i].value == str){
                cmb.selectedIndex = i;
                return;
            }
        }
    }

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

        cmbSelect(cmbModule,defaultModule);
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

                cmbSelect(cmbProject,defaultProject);
                changeProject();
                cmbProject.onchange = changeProject;
            }
            cmbSelect(cmbProject,defaultProject);
            //$("#result").html(resp);
        });
    }
    // 调用getProjectList函数
    getProjectList();

}