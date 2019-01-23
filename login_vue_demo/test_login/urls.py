from django.urls import path
from . import views

urlpatterns = [
    path('demo1/',views.demo1),
    path('demo2/',views.demo2),
    path('demo3/',views.demo3),
    path('demo4/',views.demo4),
    path('demo5/',views.demo5),
    path('demo6/',views.demo6),
    path('demo7/',views.demo7),
    path('demo8/',views.demo8),
    path('demo9/',views.demo9),
    path('demo10/',views.demo10),
    path('login_action/',views.login_action)
]
