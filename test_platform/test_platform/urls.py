from django.contrib import admin
from django.urls import path,include
from user_app import views
from project_app import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login_action/',views.login_action),
    #path('project_manage/',views.project_manage),
    path('accounts/login/', views.index),
    path('logout/', views.logout),
    path('manage/',include('project_app.urls'))
]
