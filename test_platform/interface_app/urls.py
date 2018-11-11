from django.urls import path
from interface_app import views
urlpatterns = [
    #用例管理
    path('case_manage/',views.case_manage),
    path('debug/',views.debug),
    path('api_debug/',views.api_debug),
    path('save_case/',views.save_case),
    path('get_porject_list/',views.get_porject_list),
    path('search_case_name/',views.search_case_name),
]