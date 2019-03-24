from django.contrib import admin
from django.urls import path
from interface_app.views import user_views
from interface_app.views.service.service_detail_views import ServiceDetailViews
from interface_app.views.service.service_list_views import ServiceListViews

urlpatterns = [
    # path('user/register',user_views.register_user),
    # path('user/login',user_views.login_user),
    # path('user/get', user_views.get_user),
    # path('user/temp', user_views.UserViews.as_view()),

    path('user', user_views.UserViews.as_view()),
    path('services/', ServiceListViews.as_view()),
    path('services/<int:pk>', ServiceDetailViews.as_view()),
]