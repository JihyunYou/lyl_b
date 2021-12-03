"""lyl_b URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

import lessons.views
import members.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lessons.views.index, name='index'),

    path('member/', members.views.index, name='member_index'),
    path('member/<int:member_id>/', members.views.detail, name='member_detail'),
    path('member/create_member/', members.views.MemberCreate.as_view(success_url="/member/")),
    path(
        'member/<int:member_id>/create_registration',
        members.views.RegistrationCreate.as_view(success_url="/member/")
    ),

    path('lesson/', lessons.views.list, name='lesson_list'),
    path(
        'lesson/<int:lesson_id>/',
        lessons.views.detail,
        name='lesson_detail'
    ),
    path(
        'lesson/create_lesson/',
        lessons.views.LessonCreate.as_view(success_url="/lesson/<int:lesson_id>/")
    ),
    path(
        'lesson/manage_attendance/',
        lessons.views.manage_attendance,
        name='manage_attendance'
    ),
]
