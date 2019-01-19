from django.urls import path
from . import views

urlpatterns = [
    path('demo1/',views.demo1),
    path('demo2/',views.demo2),
    path('demo3/',views.demo3),
    path('demo4/',views.demo4),
    path('login_action/',views.login_action)
]
