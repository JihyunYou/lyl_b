from django.contrib import admin
from .models import Member, Registration


class MemberAdmin(admin.ModelAdmin):
    model = Member

    # Admin 화면에서 User 리스트에 출력되는 컬럼
    list_display = (
        'name', 'gender', 'date_of_birth', 'phone_number', 'teacher_id',)

    # 화면 우측에 필터링 옵션에 출력되는 항목
    list_filter = ('gender', 'teacher_id',)

    fieldsets = (
        ('인적사항', {'fields': ('name', 'gender', 'phone_number', 'date_of_birth')}),
        ('담당강사', {'fields': ('teacher_id',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'gender')}
         ),
    )

    search_fields = ('name',)
    ordering = ('name',)


class RegistrationAdmin(admin.ModelAdmin):
    model = Registration

    # Admin 화면에서 User 리스트에 출력되는 컬럼
    list_display = (
        'member_id', 'get_member_name', 'reg_seq', 'times', 'reg_date', 'tuition',)

    # 화면 우측에 필터링 옵션에 출력되는 항목
    list_filter = ('member_id', 'reg_seq',)

    fieldsets = (
        ('등록정보', {'fields': ('member_id', 'times', 'tuition', 'reg_date')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('member_id', 'times', 'reg_date', 'tuition')}
         ),
    )

    def get_member_name(self, obj):
        return obj.member_id.name
    get_member_name.admin_order_field = "member_id"     #정렬 가능 설정
    get_member_name.short_description = "수강생"   #컬럼 헤더명 변경


admin.site.register(Member, MemberAdmin)
admin.site.register(Registration, RegistrationAdmin)
