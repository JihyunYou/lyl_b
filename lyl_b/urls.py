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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

import lessons.views
import members.views
import custom_users.views
import qna_app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lessons.views.index, name='index'),
    path('about/', custom_users.views.about, name='about'),

    path('login/', custom_users.views.login, name='login'),
    path('logout/', custom_users.views.logout, name='logout'),

    path('member/', members.views.index, name='member_index'),
    path('member/<int:member_id>/', members.views.detail, name='member_detail'),
    path(
        'member/add_member/',
        members.views.add_member,
    ),
    path('member/<int:member_id>/delete/', members.views.delete_member),
    path(
        'member/<int:member_id>/registration/<int:registration_id>/delete/',
        members.views.delete_registration
    ),

    path('lesson/', lessons.views.list, name='lesson_list'),
    path(
        'lesson/<int:lesson_id>/',
        lessons.views.detail,
        name='lesson_detail'
    ),
    path(
        'lesson/create_lesson/auto',
        lessons.views.create_default_schedule,
        name='lesson_create_auto'
    ),
    path(
        'lesson/create_lesson/',
        lessons.views.create_manual_schedule,
        name='lesson_create'
    ),
    path('lesson/<int:lesson_id>/delete/', lessons.views.delete_lesson),
    path(
        'lesson/manage_attendance/',
        lessons.views.manage_attendance,
        name='manage_attendance'
    ),

    path('qna/', qna_app.views.index, name='qna_list'),
    path('qna/create/', qna_app.views.create_qna, name='qna_create'),
    path('qna/<int:post_id>/', qna_app.views.detail, name='qna_detail'),
    path('qna/<int:post_id>/create_comment', qna_app.views.create_comment, name='qna_create_comment'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
