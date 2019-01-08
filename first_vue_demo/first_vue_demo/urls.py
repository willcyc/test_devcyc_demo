"""first_vue_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from first_vue_app import views,part_a_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('demo/',views.demo),
    path('demo2/',views.demo2),
    path('demo3/',views.demo3),
    path('demo4/',views.demo4),
    path('search/',views.search),
    path('part_a/',part_a_views.part_a),
    path('part_b/',part_a_views.part_b),
    path('part_c/',part_a_views.part_c),
    path('part_d/',part_a_views.part_d),
    path('part_e/', part_a_views.part_e),
    path('get_array/',part_a_views.get_array),
    path('get_json/',part_a_views.get_json),
]
