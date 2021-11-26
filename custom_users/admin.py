from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import Group

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Users

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Users

    # Admin User 화면에서 User 리스트에 출력되는 컬럼
    list_display = ('email', 'full_name', 'gender', 'phone_number', 'user_grade', 'is_admin', 'is_active',)

    # 화면 우측에 필터링 옵션에 출력되는 항목
    list_filter = ('gender', 'user_grade', 'is_admin', 'is_active',)

    fieldsets = (
        ('필수정보', {'fields': ('email', 'password', 'full_name')}),
        ('인적사항', {'fields': ('gender', 'phone_number')}),
        ('권한설정', {'fields': ('user_grade', 'is_admin', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'full_name', 'is_admin', 'is_active')}
         ),
    )
    #   add_fieldsets 의 내용을 아래와 같이 하면 회원가입시 필드 에러 발생
    # add_fieldsets = (
    #     ('필수정보', {'fields': ('email', 'password', 'full_name')}),
    #     ('인적사항', {'fields': ('gender', 'phone_number')}),
    #     ('권한설정', {'fields': ('user_grade', 'is_admin', 'is_active')}),
    # )

    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Users, CustomUserAdmin)
admin.site.unregister(Group)