from django.urls import path
from interface_app.views import testcase_views,testcase_api,testtask_views,testtask_api
urlpatterns = [
    #用例管理
    path('case_manage/',testcase_views.case_manage),
    path('add_case/',testcase_views.add_case),
    path('search_case_name/',testcase_views.search_case_name),
    path("debug_case/<int:cid>/",testcase_views.debug_case),
    path('delete_case/<int:cid>/',testcase_views.delete_case),

    #用例管理-由JS调用的接口
    path('get_porject_list/', testcase_api.get_porject_list),
    path('api_debug/', testcase_api.api_debug),
    path('save_case/', testcase_api.save_case),
    path('update_case/', testcase_api.update_case),
    path('get_case_info/', testcase_api.get_case_info),
    path('api_assert/', testcase_api.api_assert),


    #任务管理
    path('task_manage/',testtask_views.task_manage),
    path('add_task/',testtask_views.add_task),
    path('run_task/<int:tid>/',testtask_views.run_task),

    # 任务管理--由JS调用的接口
    path('get_case_list', testcase_api.get_case_list),
    path('save_task_data/',testtask_api.save_task_data),
]